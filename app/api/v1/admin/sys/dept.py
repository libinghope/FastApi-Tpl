from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, desc

from app.api import deps
from app.models.sys.dept import SysDept
from app.models.sys.user import SysUser
from app.schemas.sys.dept import (
    DeptCreate,
    DeptUpdate,
    DeptResponse,
    DeptTree,
    DeleteObjsForm,
)
from app.schemas.response import ResponseSchema
from app.core.codes import ErrorCode

router = APIRouter()


@router.get("/tree", response_model=ResponseSchema[List[DeptTree]])
async def get_dept_tree(
    name: Optional[str] = None,
    status: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    """
    Get department tree
    """
    stmt = select(SysDept).order_by(SysDept.sort)
    if name:
        stmt = stmt.where(SysDept.name.like(f"%{name}%"))
    if status is not None:
        stmt = stmt.where(SysDept.status == status)

    result = await db.execute(stmt)
    depts = result.scalars().all()

    # Build tree
    return ResponseSchema(result=build_dept_tree(depts, 0))


@router.get("/options", response_model=ResponseSchema)
async def get_dept_options(
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    """
    Get department options (tree structure)
    """
    stmt = select(SysDept).where(SysDept.status == 1).order_by(SysDept.sort)
    result = await db.execute(stmt)
    depts = result.scalars().all()

    tree = build_dept_tree(depts, 0)
    return ResponseSchema(result={"result": [dept.model_dump() for dept in tree]})


@router.post("/add", response_model=ResponseSchema)
async def add_dept(
    form: DeptCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    """
    Add department
    """
    # Check if code exists
    stmt = select(SysDept).where(SysDept.code == form.code)
    if await db.scalar(stmt):
        return ResponseSchema(
            code=ErrorCode.DEPT_ALREADY_EXISTS, message="Department code already exists"
        )

    new_dept = SysDept(**form.model_dump())
    new_dept.create_by = current_user.username

    # Handle tree path
    # If parent_id is 0, path is "0"
    # If parent_id is not 0, path is "parent_path,parent_id"
    if new_dept.parent_id == 0:
        new_dept.tree_path = "0"
    else:
        parent_stmt = select(SysDept).where(SysDept.id == new_dept.parent_id)
        parent = await db.scalar(parent_stmt)
        if not parent:
            return ResponseSchema(
                code=ErrorCode.PARENT_DEPT_NOT_FOUND,
                message="Parent department not found",
            )
        if not parent.status:  # Check if parent is disabled
            return ResponseSchema(
                code=ErrorCode.PARENT_DEPT_DISABLED,
                message="Parent department is disabled",
            )
        new_dept.tree_path = f"{parent.tree_path},{parent.id}"

    db.add(new_dept)
    await db.commit()
    return ResponseSchema(message="Success")


@router.put("/update", response_model=ResponseSchema)
async def update_dept(
    form: DeptUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    """
    Update department
    """
    dept = await db.get(SysDept, form.id)
    if not dept:
        return ResponseSchema(
            code=ErrorCode.DEPT_NOT_FOUND, message="Department not found"
        )

    if dept.id == form.parent_id:
        return ResponseSchema(
            code=ErrorCode.INVALID_ARGUMENT, message="Cannot set parent to self"
        )

    # Check code uniqueness if changed
    if form.code != dept.code:
        stmt = select(SysDept).where(SysDept.code == form.code)
        if await db.scalar(stmt):
            return ResponseSchema(
                code=ErrorCode.DEPT_ALREADY_EXISTS,
                message="Department code already exists",
            )

    # Update simple fields
    dept.name = form.name
    dept.code = form.code
    dept.sort = form.sort
    dept.status = form.status
    dept.remark = form.remark
    dept.update_by = current_user.username

    # Handle parent change
    if dept.parent_id != form.parent_id:
        if form.parent_id == 0:
            new_tree_path = "0"
        else:
            parent_stmt = select(SysDept).where(SysDept.id == form.parent_id)
            parent = await db.scalar(parent_stmt)
            if not parent:
                return ResponseSchema(
                    code=ErrorCode.PARENT_DEPT_NOT_FOUND,
                    message="Parent department not found",
                )
            new_tree_path = f"{parent.tree_path},{parent.id}"

        # Update children's tree_path?
        # Usually we need to update all children tree_paths recursively or by like query.
        # This is complex. For now let's assume simple update.
        # TODO: Update children tree_path if structure changes.
        # A simple way: find all children whose tree_path starts with old_path and replace prefix.

        old_tree_path = f"{dept.tree_path},{dept.id}"
        new_level_tree_path = f"{new_tree_path},{dept.id}"

        # We need to find all descendants
        # Descendants have tree_path like "old_tree_path,%"
        # But wait, logic:
        # Dept A (id 1, path 0). Child B (id 2, path 0,1). Child C (id 3, path 0,1,2).
        # Move B to Root. B (id 2, path 0). C (id 3, path 0,2).
        # Yes, we need to update descendants.

        dept.parent_id = form.parent_id
        dept.tree_path = new_tree_path

        # Find descendants
        descendants_stmt = select(SysDept).where(
            SysDept.tree_path.like(f"{old_tree_path}%")
        )
        descendants_result = await db.execute(descendants_stmt)
        descendants = descendants_result.scalars().all()

        for child in descendants:
            # Replace prefix
            # child.tree_path was "0,1,2" (old_tree_path "0,1")
            # new_level_tree_path is "0,1" (if just moved same place)
            # wait.
            # old descendant path starts with old_tree_path.
            # new descendant path should starts with new_level_tree_path.
            suffix = child.tree_path[len(old_tree_path) :]
            child.tree_path = f"{new_level_tree_path}{suffix}"

    await db.commit()
    return ResponseSchema(message="Success")


@router.post("/delete", response_model=ResponseSchema)
async def delete_dept(
    form: DeleteObjsForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    """
    Delete department
    """
    # Check if any dept has children
    stmt = select(SysDept).where(SysDept.parent_id.in_(form.ids))
    if await db.scalar(stmt):
        return ResponseSchema(
            code=ErrorCode.OPERATION_FAILED,
            message="Cannot delete department with children",
        )

    # Check if assigned to users?
    user_stmt = select(SysUser).where(SysUser.dept_id.in_(form.ids))
    if await db.scalar(user_stmt):
        return ResponseSchema(
            code=ErrorCode.OPERATION_FAILED,
            message="Cannot delete department with users",
        )

    await db.execute(delete(SysDept).where(SysDept.id.in_(form.ids)))
    await db.commit()
    return ResponseSchema(message="Success")


def build_dept_tree(depts: List[SysDept], parent_id: int) -> List[DeptTree]:
    tree = []
    for dept in depts:
        if dept.parent_id == parent_id:
            node = DeptTree.model_validate(dept)
            children = build_dept_tree(depts, dept.id)
            if children:
                node.children = children
            tree.append(node)
    return tree
