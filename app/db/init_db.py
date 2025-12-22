from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.sys.user import SysUser, SysUserRoleRef
from app.models.sys.role import SysRole

async def init_db(db: AsyncSession) -> None:
    # 1. Create root role
    result = await db.execute(select(SysRole).where(SysRole.code == "admin"))
    role = result.scalars().first()
    if not role:
        role = SysRole(
            name="Super Admin",
            code="admin",
            sort=1,
            status=1,
            data_scope=1,
            remark="Super User Role"
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        print("Role 'admin' created.")
    else:
        print("Role 'admin' already exists.")

    # 2. Create root user
    result = await db.execute(select(SysUser).where(SysUser.username == settings.MYSQL_USER))
    user = result.scalars().first()
    if not user:
        user = SysUser(
            username=settings.MYSQL_USER,
            nickname="Root",
            hashed_password=get_password_hash(settings.MYSQL_PASSWORD),
            email="root@example.com",
            is_superuser=True,
            is_active=True,
            status=1,
            remark="Initial Super User"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        print(f"User '{settings.MYSQL_USER}' created.")
        
        # 3. Assign role to user
        user_role = SysUserRoleRef(
            user_id=user.id,
            role_id=role.id
        )
        db.add(user_role)
        await db.commit()
        print(f"Role 'admin' assigned to user '{settings.MYSQL_USER}'.")
        
    else:
        print(f"User '{settings.MYSQL_USER}' already exists.")
