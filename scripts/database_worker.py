import asyncio
import sys
import os

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.sys.dept import SysDept
from app.models.sys.dictionary import SysDict, SysDictItem
from app.models.sys.menu import SysMenu, SysRoleMenu
from app.models.sys.role import SysRole
from app.models.sys.user import SysUserRoleRef, SysUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.globals.enum import RoleDataScope, MenuType


async def create_initial_data():
    async with SessionLocal() as db:
        await create_all_data(db)
        await db.commit()


async def create_all_data(db: AsyncSession):
    create_sys_dict(db)
    create_sys_dict_data(db)
    create_sys_dept(db)
    create_sys_menu(db)
    create_sys_role(db)
    create_sys_role_menu(db)
    create_sys_user(db)
    create_sys_user_role(db)


def create_sys_user_role(db: AsyncSession):
    userRole1 = SysUserRoleRef(user_id=1, role_id=1)
    userRole2 = SysUserRoleRef(user_id=2, role_id=2)
    userRole3 = SysUserRoleRef(user_id=3, role_id=3)
    db.add_all([userRole1, userRole2, userRole3])


def create_sys_user(db: AsyncSession):
    user1 = SysUser(
        id=1,
        username="root",
        email="root@test.com",
        nickname="有来技术",
        hashed_password=get_password_hash("12345678"),
        phone_number="18866668888",
        is_superuser=True,
    )
    user2 = SysUser(
        id=2,
        username="admin",
        email="admin@test.com",
        dept_id="1",
        nickname="系统管理员",
        hashed_password=get_password_hash("12345678"),
        phone_number="18866668888",
        is_superuser=True,
    )
    user3 = SysUser(
        id=3,
        username="test",
        email="test@test.com",
        dept_id="3",
        nickname="测试小用户",
        hashed_password=get_password_hash("12345678"),
        phone_number="18866668888",
    )
    db.add_all([user1, user2, user3])


def create_sys_role_menu(db: AsyncSession):
    roleMenu1 = SysRoleMenu(role_id=2, menu_id=1)
    roleMenu2 = SysRoleMenu(role_id=2, menu_id=2)
    roleMenu3 = SysRoleMenu(role_id=2, menu_id=3)
    roleMenu4 = SysRoleMenu(role_id=2, menu_id=4)
    roleMenu5 = SysRoleMenu(role_id=2, menu_id=5)
    roleMenu6 = SysRoleMenu(role_id=2, menu_id=6)
    roleMenu7 = SysRoleMenu(role_id=2, menu_id=20)
    roleMenu8 = SysRoleMenu(role_id=2, menu_id=21)
    roleMenu9 = SysRoleMenu(role_id=2, menu_id=22)
    roleMenu10 = SysRoleMenu(role_id=2, menu_id=23)
    roleMenu11 = SysRoleMenu(role_id=2, menu_id=24)
    roleMenu12 = SysRoleMenu(role_id=2, menu_id=26)
    roleMenu13 = SysRoleMenu(role_id=2, menu_id=30)
    roleMenu14 = SysRoleMenu(role_id=2, menu_id=31)
    roleMenu15 = SysRoleMenu(role_id=2, menu_id=32)
    roleMenu16 = SysRoleMenu(role_id=2, menu_id=33)
    roleMenu17 = SysRoleMenu(role_id=2, menu_id=36)
    roleMenu18 = SysRoleMenu(role_id=2, menu_id=37)
    roleMenu19 = SysRoleMenu(role_id=2, menu_id=38)
    roleMenu20 = SysRoleMenu(role_id=2, menu_id=39)
    roleMenu21 = SysRoleMenu(role_id=2, menu_id=40)
    roleMenu22 = SysRoleMenu(role_id=2, menu_id=41)
    roleMenu23 = SysRoleMenu(role_id=2, menu_id=70)
    roleMenu24 = SysRoleMenu(role_id=2, menu_id=71)
    roleMenu25 = SysRoleMenu(role_id=2, menu_id=72)
    roleMenu26 = SysRoleMenu(role_id=2, menu_id=73)
    roleMenu27 = SysRoleMenu(role_id=2, menu_id=74)
    roleMenu28 = SysRoleMenu(role_id=2, menu_id=75)
    roleMenu29 = SysRoleMenu(role_id=2, menu_id=76)
    roleMenu30 = SysRoleMenu(role_id=2, menu_id=77)
    roleMenu31 = SysRoleMenu(role_id=2, menu_id=78)
    roleMenu32 = SysRoleMenu(role_id=2, menu_id=79)
    roleMenu33 = SysRoleMenu(role_id=2, menu_id=81)
    roleMenu34 = SysRoleMenu(role_id=2, menu_id=84)
    roleMenu35 = SysRoleMenu(role_id=2, menu_id=85)
    roleMenu36 = SysRoleMenu(role_id=2, menu_id=86)
    roleMenu37 = SysRoleMenu(role_id=2, menu_id=87)
    roleMenu38 = SysRoleMenu(role_id=2, menu_id=88)
    roleMenu39 = SysRoleMenu(role_id=2, menu_id=89)
    roleMenu40 = SysRoleMenu(role_id=2, menu_id=90)
    roleMenu41 = SysRoleMenu(role_id=2, menu_id=91)
    roleMenu42 = SysRoleMenu(role_id=2, menu_id=95)
    roleMenu43 = SysRoleMenu(role_id=2, menu_id=97)
    roleMenu44 = SysRoleMenu(role_id=2, menu_id=102)
    roleMenu45 = SysRoleMenu(role_id=2, menu_id=105)
    roleMenu46 = SysRoleMenu(role_id=2, menu_id=106)
    roleMenu47 = SysRoleMenu(role_id=2, menu_id=107)
    roleMenu48 = SysRoleMenu(role_id=2, menu_id=108)
    roleMenu49 = SysRoleMenu(role_id=2, menu_id=109)
    roleMenu50 = SysRoleMenu(role_id=2, menu_id=110)
    roleMenu51 = SysRoleMenu(role_id=2, menu_id=111)
    roleMenu52 = SysRoleMenu(role_id=2, menu_id=112)
    roleMenu53 = SysRoleMenu(role_id=2, menu_id=114)
    roleMenu54 = SysRoleMenu(role_id=2, menu_id=115)
    roleMenu55 = SysRoleMenu(role_id=2, menu_id=116)
    roleMenu56 = SysRoleMenu(role_id=2, menu_id=117)
    roleMenu57 = SysRoleMenu(role_id=2, menu_id=118)
    roleMenu58 = SysRoleMenu(role_id=2, menu_id=119)
    roleMenu59 = SysRoleMenu(role_id=2, menu_id=120)
    roleMenu60 = SysRoleMenu(role_id=2, menu_id=121)
    roleMenu61 = SysRoleMenu(role_id=2, menu_id=122)
    roleMenu62 = SysRoleMenu(role_id=2, menu_id=123)
    roleMenu63 = SysRoleMenu(role_id=2, menu_id=124)
    roleMenu64 = SysRoleMenu(role_id=2, menu_id=125)
    roleMenu65 = SysRoleMenu(role_id=2, menu_id=126)
    roleMenu66 = SysRoleMenu(role_id=2, menu_id=127)
    roleMenu67 = SysRoleMenu(role_id=2, menu_id=128)
    roleMenu68 = SysRoleMenu(role_id=2, menu_id=129)
    roleMenu69 = SysRoleMenu(role_id=2, menu_id=130)
    roleMenu70 = SysRoleMenu(role_id=2, menu_id=131)
    roleMenu71 = SysRoleMenu(role_id=2, menu_id=132)
    roleMenu72 = SysRoleMenu(role_id=2, menu_id=133)
    roleMenu73 = SysRoleMenu(role_id=2, menu_id=134)
    roleMenu74 = SysRoleMenu(role_id=2, menu_id=135)
    roleMenu75 = SysRoleMenu(role_id=2, menu_id=136)
    roleMenu76 = SysRoleMenu(role_id=2, menu_id=137)
    roleMenu77 = SysRoleMenu(role_id=2, menu_id=138)
    db.add_all(
        [
            roleMenu1,
            roleMenu2,
            roleMenu3,
            roleMenu4,
            roleMenu5,
            roleMenu6,
            roleMenu7,
            roleMenu8,
            roleMenu9,
            roleMenu10,
            roleMenu11,
            roleMenu12,
            roleMenu13,
            roleMenu14,
            roleMenu15,
            roleMenu16,
            roleMenu17,
            roleMenu18,
            roleMenu19,
            roleMenu20,
            roleMenu21,
            roleMenu22,
            roleMenu23,
            roleMenu24,
            roleMenu25,
            roleMenu26,
            roleMenu27,
            roleMenu28,
            roleMenu29,
            roleMenu30,
            roleMenu31,
            roleMenu32,
            roleMenu33,
            roleMenu34,
            roleMenu35,
            roleMenu36,
            roleMenu37,
            roleMenu38,
            roleMenu39,
            roleMenu40,
            roleMenu41,
            roleMenu42,
            roleMenu43,
            roleMenu44,
            roleMenu45,
            roleMenu46,
            roleMenu47,
            roleMenu48,
            roleMenu49,
            roleMenu50,
            roleMenu51,
            roleMenu52,
            roleMenu53,
            roleMenu54,
            roleMenu55,
            roleMenu56,
            roleMenu57,
            roleMenu58,
            roleMenu59,
            roleMenu60,
            roleMenu61,
            roleMenu62,
            roleMenu63,
            roleMenu64,
            roleMenu65,
            roleMenu66,
            roleMenu67,
            roleMenu68,
            roleMenu69,
            roleMenu70,
            roleMenu71,
            roleMenu72,
            roleMenu73,
            roleMenu74,
            roleMenu75,
            roleMenu76,
            roleMenu77,
        ]
    )


def create_sys_role(db: AsyncSession):
    role1 = SysRole(
        id=1, name="超级管理员", code="ROOT", sort=1, data_scope=RoleDataScope.ALL
    )
    role2 = SysRole(
        id=2,
        name="系统管理员",
        code="ADMIN",
        sort=2,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role3 = SysRole(
        id=3, name="访问游客", code="GUEST", sort=3, data_scope=RoleDataScope.DEPT
    )
    role4 = SysRole(
        id=4,
        name="系统管理员1",
        code="ADMIN1",
        sort=4,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role5 = SysRole(
        id=5,
        name="系统管理员2",
        code="ADMIN2",
        sort=5,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role6 = SysRole(
        id=6,
        name="系统管理员3",
        code="ADMIN3",
        sort=6,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role7 = SysRole(
        id=7,
        name="系统管理员4",
        code="ADMIN4",
        sort=7,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role8 = SysRole(
        id=8,
        name="系统管理员5",
        code="ADMIN5",
        sort=8,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role9 = SysRole(
        id=9,
        name="系统管理员6",
        code="ADMIN6",
        sort=9,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role10 = SysRole(
        id=10,
        name="系统管理员7",
        code="ADMIN7",
        sort=10,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role11 = SysRole(
        id=11,
        name="系统管理员8",
        code="ADMIN8",
        sort=11,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    role12 = SysRole(
        id=12,
        name="系统管理员9",
        code="ADMIN9",
        sort=12,
        data_scope=RoleDataScope.DEPT_AND_CHILD,
    )
    db.add_all(
        [
            role1,
            role2,
            role3,
            role4,
            role5,
            role6,
            role7,
            role8,
            role9,
            role10,
            role11,
            role12,
        ]
    )


def create_sys_menu(db: AsyncSession):
    menu1 = SysMenu(
        id=1,
        parent_id=0,
        tree_path="0",
        name="系统管理",
        type=MenuType.CATALOG,
        route_name="",
        route_path="/system",
        component="Layout",
        visible=1,
        sort=1,
        icon="system",
        redirect="/system/user",
    )
    # INSERT INTO `sys_menu` VALUES (2, 1, '0,1', '用户管理', 1, 'User', 'user', 'system/user/index', NULL, NULL, 1, 1, 1, 'el-icon-User', NULL, now(), now(), NULL);
    menu2 = SysMenu(
        id=2,
        parent_id=1,
        tree_path="0,1",
        name="用户管理",
        type=MenuType.MENU,
        route_name="User",
        route_path="user",
        component="system/user/index",
        visible=1,
        sort=1,
        icon="el-icon-User",
    )

    menu3 = SysMenu(
        id=3,
        parent_id=1,
        tree_path="0,1",
        name="角色管理",
        type=MenuType.MENU,
        route_name="Role",
        route_path="role",
        component="system/role/index",
        visible=1,
        sort=2,
        icon="role",
    )
    # INSERT INTO `sys_menu` VALUES (4, 1, '0,1', '菜单管理', 1, 'Menu', 'menu', 'system/menu/index', NULL, NULL, 1, 1, 3, 'menu', NULL, now(), now(), NULL);
    menu4 = SysMenu(
        id=4,
        parent_id=1,
        tree_path="0,1",
        name="菜单管理",
        type=MenuType.MENU,
        route_name="Menu",
        route_path="menu",
        component="system/menu/index",
        visible=1,
        sort=3,
        icon="menu",
    )
    # INSERT INTO `sys_menu` VALUES (5, 1, '0,1', '部门管理', 1, 'Dept', 'dept', 'system/dept/index', NULL, NULL, 1, 1, 4, 'tree', NULL, now(), now(), NULL);
    menu5 = SysMenu(
        id=5,
        parent_id=1,
        tree_path="0,1",
        name="部门管理",
        type=MenuType.MENU,
        route_name="Dept",
        route_path="dept",
        component="system/dept/index",
        visible=1,
        sort=4,
        icon="tree",
    )
    # INSERT INTO `sys_menu` VALUES (6, 1, '0,1', '字典管理', 1, 'Dict', 'dict', 'system/dict/index', NULL, NULL, 1, 1, 5, 'dict', NULL, now(), now(), NULL);
    menu6 = SysMenu(
        id=6,
        parent_id=1,
        tree_path="0,1",
        name="字典管理",
        type=MenuType.MENU,
        route_name="Dict",
        route_path="dict",
        component="system/dict/index",
        visible=1,
        sort=5,
        icon="dict",
    )
    # INSERT INTO `sys_menu` VALUES (20, 0, '0', '多级菜单', 2, NULL, '/multi-level', 'Layout', NULL, 1, NULL, 1, 9, 'cascader', '', now(), now(), NULL);
    menu7 = SysMenu(
        id=20,
        parent_id=0,
        tree_path="0",
        name="多级菜单",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/multi-level",
        component="Layout",
        visible=1,
        sort=9,
        icon="cascader",
        redirect="",
    )
    # INSERT INTO `sys_menu` VALUES (21, 20, '0,20', '菜单一级', 1, NULL, 'multi-level1', 'demo/multi-level/level1', NULL, 1, NULL, 1, 1, '', '', now(), now(), NULL);
    menu8 = SysMenu(
        id=21,
        parent_id=20,
        tree_path="0,20",
        name="菜单一级",
        type=MenuType.MENU,
        route_name=None,
        route_path="multi-level1",
        component="demo/multi-level/level1",
        visible=1,
        sort=1,
        icon="",
    )
    # INSERT INTO `sys_menu` VALUES (22, 21, '0,20,21', '菜单二级', 1, NULL, 'multi-level2', 'demo/multi-level/children/level2', NULL, 0, NULL, 1, 1, '', NULL, now(), now(), NULL);
    menu9 = SysMenu(
        id=22,
        parent_id=21,
        tree_path="0,20,21",
        name="菜单二级",
        type=MenuType.MENU,
        route_name=None,
        route_path="multi-level2",
        component="demo/multi-level/children/level2",
        visible=1,
        sort=2,
        icon="",
    )
    # INSERT INTO `sys_menu` VALUES (23, 22, '0,20,21,22', '菜单三级-1', 1, NULL, 'multi-level3-1', 'demo/multi-level/children/children/level3-1', NULL, 0, 1, 1, 1, '', '', now(), now(), NULL);
    menu10 = SysMenu(
        id=23,
        parent_id=22,
        tree_path="0,20,21,22",
        name="菜单三级-1",
        type=MenuType.MENU,
        route_name=None,
        route_path="multi-level3-1",
        component="demo/multi-level/children/children/level3-1",
        visible=1,
        sort=1,
        icon="",
    )
    # INSERT INTO `sys_menu` VALUES (24, 22, '0,20,21,22', '菜单三级-2', 1, NULL, 'multi-level3-2', 'demo/multi-level/children/children/level3-2', NULL, 0, 1, 1, 2, '', '', now(), now(), NULL);
    menu11 = SysMenu(
        id=24,
        parent_id=22,
        tree_path="0,20,21,22",
        name="菜单三级-2",
        type=MenuType.MENU,
        route_name=None,
        route_path="multi-level3-2",
        component="demo/multi-level/children/children/level3-2",
        visible=1,
        sort=2,
        icon="",
    )
    # INSERT INTO `sys_menu` VALUES (26, 0, '0', '平台文档', 2, NULL, '/doc', 'Layout', NULL, NULL, NULL, 1, 8, 'document', 'https://juejin.cn/post/7228990409909108793', now(), now(), NULL);
    menu12 = SysMenu(
        id=26,
        parent_id=0,
        tree_path="0",
        name="平台文档",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/doc",
        component="Layout",
        visible=1,
        sort=8,
        icon="document",
        redirect="",
    )
    # INSERT INTO `sys_menu` VALUES (30, 26, '0,26', '文档(外链)', 3, NULL, 'https://juejin.cn/post/7228990409909108793', '', NULL, NULL, NULL, 1, 2, 'link', '', now(), now(), NULL);
    menu13 = SysMenu(
        id=30,
        parent_id=26,
        tree_path="0,26",
        name="文档(外链)",
        type=MenuType.EXTLINK,
        route_name=None,
        route_path="https://juejin.cn/post/7228990409909108793",
        component="",
        visible=1,
        sort=2,
        icon="link",
        redirect="",
    )
    # INSERT INTO `sys_menu` VALUES (31, 2, '0,1,2', '用户新增', 4, NULL, '', NULL, 'sys:user:add', NULL, NULL, 1, 1, '', '', now(), now(), NULL);
    menu14 = SysMenu(
        id=31,
        parent_id=2,
        tree_path="0,1,2",
        name="用户新增",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=1,
        icon="",
        perm="sys:user:add",
    )
    # INSERT INTO `sys_menu` VALUES (32, 2, '0,1,2', '用户编辑', 4, NULL, '', NULL, 'sys:user:edit', NULL, NULL, 1, 2, '', '', now(), now(), NULL);
    menu15 = SysMenu(
        id=32,
        parent_id=2,
        tree_path="0,1,2",
        name="用户编辑",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=2,
        icon="",
        perm="sys:user:edit",
    )
    # INSERT INTO `sys_menu` VALUES (33, 2, '0,1,2', '用户删除', 4, NULL, '', NULL, 'sys:user:delete', NULL, NULL, 1, 3, '', '', now(), now(), NULL);
    menu16 = SysMenu(
        id=33,
        parent_id=2,
        tree_path="0,1,2",
        name="用户删除",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:user:delete",
    )
    # INSERT INTO `sys_menu` VALUES (36, 0, '0', '组件封装', 2, NULL, '/component', 'Layout', NULL, NULL, NULL, 1, 10, 'menu', '', now(), now(), NULL);
    menu17 = SysMenu(
        id=36,
        parent_id=0,
        tree_path="0",
        name="组件封装",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/component",
        component="Layout",
        visible=1,
        sort=10,
        icon="menu",
        redirect="",
    )
    # INSERT INTO `sys_menu` VALUES (37, 36, '0,36', '富文本编辑器', 1, NULL, 'wang-editor', 'demo/wang-editor', NULL, NULL, 1, 1, 2, '', '', NULL, NULL, NULL);
    menu18 = SysMenu(
        id=37,
        parent_id=36,
        tree_path="0,36",
        name="富文本编辑器",
        type=MenuType.MENU,
        route_name=None,
        route_path="wang-editor",
        component="demo/wang-editor",
        visible=1,
        sort=2,
        icon="",
    )
    # INSERT INTO `sys_menu` VALUES (38, 36, '0,36', '图片上传', 1, NULL, 'upload', 'demo/upload', NULL, NULL, 1, 1, 3, '', '', now(), now(), NULL);
    menu19 = SysMenu(
        id=38,
        parent_id=36,
        tree_path="0,36",
        name="图片上传",
        type=MenuType.MENU,
        route_name=None,
        route_path="upload",
        component="demo/upload",
        visible=1,
        sort=3,
        icon="",
    )
    menu20 = SysMenu(
        id=39,
        parent_id=36,
        tree_path="0,36",
        name="图标选择器",
        type=MenuType.MENU,
        route_name=None,
        route_path="icon-selector",
        component="demo/icon-selector",
        visible=1,
        sort=4,
        icon="",
    )
    menu21 = SysMenu(
        id=40,
        parent_id=0,
        tree_path="0",
        name="接口文档",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/api",
        component="Layout",
        visible=1,
        sort=7,
        icon="api",
        redirect="",
    )
    menu22 = SysMenu(
        id=41,
        parent_id=40,
        tree_path="0,40",
        name="Apifox",
        type=MenuType.MENU,
        route_name=None,
        route_path="apifox",
        component="demo/api/apifox",
        visible=1,
        sort=1,
        icon="api",
        redirect="",
    )
    menu23 = SysMenu(
        id=70,
        parent_id=3,
        tree_path="0,1,3",
        name="角色新增",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=1,
        icon="",
        perm="sys:role:add",
    )
    menu24 = SysMenu(
        id=71,
        parent_id=3,
        tree_path="0,1,3",
        name="角色编辑",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=2,
        icon="",
        perm="sys:role:edit",
    )
    menu25 = SysMenu(
        id=72,
        parent_id=3,
        tree_path="0,1,3",
        name="角色删除",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:role:delete",
    )
    menu26 = SysMenu(
        id=73,
        parent_id=4,
        tree_path="0,1,4",
        name="菜单新增",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=1,
        icon="",
        perm="sys:menu:add",
    )
    menu27 = SysMenu(
        id=74,
        parent_id=4,
        tree_path="0,1,4",
        name="菜单编辑",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:menu:edit",
    )
    menu28 = SysMenu(
        id=75,
        parent_id=4,
        tree_path="0,1,4",
        name="菜单删除",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:menu:delete",
    )
    menu29 = SysMenu(
        id=76,
        parent_id=5,
        tree_path="0,1,5",
        name="部门新增",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=1,
        icon="",
        perm="sys:dept:add",
    )
    menu30 = SysMenu(
        id=78,
        parent_id=5,
        tree_path="0,1,5",
        name="部门编辑",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=2,
        icon="",
        perm="sys:dept:edit",
    )
    menu31 = SysMenu(
        id=79,
        parent_id=5,
        tree_path="0,1,5",
        name="部门删除",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:dept:delete",
    )
    menu32 = SysMenu(
        id=80,
        parent_id=6,
        tree_path="0,1,6",
        name="字典新增",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=1,
        icon="",
        perm="sys:dict:add",
    )
    menu33 = SysMenu(
        id=81,
        parent_id=6,
        tree_path="0,1,6",
        name="字典编辑",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=2,
        icon="",
        perm="sys:dict:edit",
    )
    menu34 = SysMenu(
        id=84,
        parent_id=6,
        tree_path="0,1,6",
        name="字典删除",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:dict:delete",
    )
    menu35 = SysMenu(
        id=88,
        parent_id=2,
        tree_path="0,1,2",
        name="重置密码",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=4,
        icon="",
        perm="sys:user:password:reset",
    )
    menu36 = SysMenu(
        id=89,
        parent_id=0,
        tree_path="0",
        name="功能演示",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/function",
        component="Layout",
        visible=1,
        sort=12,
        icon="menu",
        redirect="",
    )
    menu37 = SysMenu(
        id=90,
        parent_id=89,
        tree_path="0,89",
        name="Websocket",
        type=MenuType.MENU,
        route_name=None,
        route_path="/function/websocket",
        component="demo/websocket",
        visible=1,
        sort=3,
        icon="",
        redirect="",
    )
    menu38 = SysMenu(
        id=91,
        parent_id=89,
        tree_path="0,89",
        name="敬请期待...",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="other/:id",
        component="demo/other",
        visible=1,
        sort=4,
        icon="",
        redirect="",
    )
    menu39 = SysMenu(
        id=95,
        parent_id=89,
        tree_path="0,89",
        name="字典组件",
        type=MenuType.MENU,
        route_name=None,
        route_path="dict-demo",
        component="demo/dict",
        visible=1,
        sort=4,
        icon="",
    )
    menu40 = SysMenu(
        id=97,
        parent_id=89,
        tree_path="0,89",
        name="Icons",
        type=MenuType.MENU,
        route_name=None,
        route_path="icon-demo",
        component="demo/icons",
        visible=1,
        sort=2,
        icon="el-icon-Notification",
    )
    menu41 = SysMenu(
        id=102,
        parent_id=26,
        tree_path="0,26",
        name="文档(内嵌)",
        type=MenuType.EXTLINK,
        route_name=None,
        route_path="internal-doc",
        component="demo/internal-doc",
        visible=1,
        sort=1,
        icon="document",
        redirect="",
    )
    menu42 = SysMenu(
        id=105,
        parent_id=2,
        tree_path="0,1,2",
        name="用户查询",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=0,
        icon="",
        perm="sys:user:query",
    )
    menu43 = SysMenu(
        id=106,
        parent_id=2,
        tree_path="0,1,2",
        name="用户导入",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=5,
        icon="",
        perm="sys:user:import",
    )
    menu44 = SysMenu(
        id=107,
        parent_id=2,
        tree_path="0,1,2",
        name="用户导出",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=6,
        icon="",
        perm="sys:user:export",
    )
    menu45 = SysMenu(
        id=108,
        parent_id=36,
        tree_path="0,36",
        name="增删改查",
        type=MenuType.MENU,
        route_name=None,
        route_path="curd",
        component="demo/curd/index",
        visible=1,
        sort=0,
        icon="",
    )
    menu46 = SysMenu(
        id=109,
        parent_id=36,
        tree_path="0,36",
        name="列表选择器",
        type=MenuType.MENU,
        route_name=None,
        route_path="table-select",
        component="demo/table-select/index",
        visible=1,
        sort=1,
        icon="",
    )
    menu47 = SysMenu(
        id=110,
        parent_id=0,
        tree_path="0",
        name="路由参数",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/route-param",
        component="Layout",
        visible=1,
        sort=11,
        icon="el-icon-ElementPlus",
        redirect="",
    )
    menu48 = SysMenu(
        id=111,
        parent_id=110,
        tree_path="0,110",
        name="参数(type=1)",
        type=MenuType.MENU,
        route_name=None,
        route_path="route-param-type1",
        component="demo/route-param",
        visible=1,
        sort=1,
        icon="el-icon-Star",
        redirect="",
        params='{"type": "1"}',
    )
    menu49 = SysMenu(
        id=112,
        parent_id=110,
        tree_path="0,110",
        name="参数(type=2)",
        type=MenuType.MENU,
        route_name=None,
        route_path="route-param-type2",
        component="demo/route-param",
        visible=1,
        sort=2,
        icon="el-icon-StarFilled",
        redirect="",
        params='{"type": "2"}',
    )
    menu50 = SysMenu(
        id=117,
        parent_id=1,
        tree_path="0,1",
        name="系统日志",
        type=MenuType.MENU,
        route_name="Log",
        route_path="log",
        component="system/log/index",
        visible=1,
        sort=6,
        icon="document",
        redirect="",
    )
    menu51 = SysMenu(
        id=118,
        parent_id=0,
        tree_path="0",
        name="系统工具",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/codegen",
        component="Layout",
        visible=1,
        sort=2,
        icon="menu",
        redirect="",
    )
    menu52 = SysMenu(
        id=119,
        parent_id=118,
        tree_path="0,118",
        name="代码生成",
        type=MenuType.MENU,
        route_name="Codegen",
        route_path="codegen",
        component="codegen/index",
        visible=1,
        sort=1,
        icon="code",
        redirect="",
    )
    menu53 = SysMenu(
        id=120,
        parent_id=1,
        tree_path="0,1",
        name="系统配置",
        type=MenuType.MENU,
        route_name="Config",
        route_path="config",
        component="system/config/index",
        visible=1,
        sort=7,
        icon="setting",
        redirect="",
    )
    menu54 = SysMenu(
        id=121,
        parent_id=120,
        tree_path="0,1,120",
        name="查询系统配置",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=1,
        icon="",
        perm="sys:config:query",
    )
    menu55 = SysMenu(
        id=122,
        parent_id=120,
        tree_path="0,1,120",
        name="新增系统配置",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=2,
        icon="",
        perm="sys:config:add",
    )
    menu56 = SysMenu(
        id=123,
        parent_id=120,
        tree_path="0,1,120",
        name="修改系统配置",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:config:update",
    )
    menu57 = SysMenu(
        id=124,
        parent_id=120,
        tree_path="0,1,120",
        name="删除系统配置",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=4,
        icon="",
        perm="sys:config:delete",
    )
    menu58 = SysMenu(
        id=125,
        parent_id=120,
        tree_path="0,1,120",
        name="刷新系统配置",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=5,
        icon="",
        perm="sys:config:refresh",
    )
    menu59 = SysMenu(
        id=126,
        parent_id=1,
        tree_path="0,1",
        name="通知公告",
        type=MenuType.MENU,
        route_name="Notice",
        route_path="notice",
        component="system/notice/index",
        visible=1,
        sort=9,
        icon="",
        redirect="",
    )
    menu60 = SysMenu(
        id=127,
        parent_id=126,
        tree_path="0,1,126",
        name="查询",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=1,
        icon="",
        perm="sys:notice:query",
    )
    menu61 = SysMenu(
        id=128,
        parent_id=126,
        tree_path="0,1,126",
        name="新增",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=2,
        icon="",
        perm="sys:notice:add",
    )
    menu62 = SysMenu(
        id=129,
        parent_id=126,
        tree_path="0,1,126",
        name="编辑",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=3,
        icon="",
        perm="sys:notice:edit",
    )
    menu63 = SysMenu(
        id=130,
        parent_id=126,
        tree_path="0,1,126",
        name="删除",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=4,
        icon="",
        perm="sys:notice:delete",
    )
    menu64 = SysMenu(
        id=133,
        parent_id=126,
        tree_path="0,1,126",
        name="发布",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=5,
        icon="",
        perm="sys:notice:publish",
    )
    menu65 = SysMenu(
        id=134,
        parent_id=126,
        tree_path="0,1,126",
        name="撤回",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=6,
        icon="",
        perm="sys:notice:revoke",
    )
    menu66 = SysMenu(
        id=135,
        parent_id=1,
        tree_path="0,1",
        name="字典数据",
        type=MenuType.MENU,
        route_name="DictData",
        route_path="dict-item",
        component="system/dict/dict-item",
        visible=0,
        sort=6,
        icon="",
        redirect="",
    )
    menu67 = SysMenu(
        id=136,
        parent_id=135,
        tree_path="0,1,135",
        name="字典数据新增",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=4,
        icon="",
        perm="sys:dict-data:add",
    )
    menu68 = SysMenu(
        id=139,
        parent_id=135,
        tree_path="0,1,135",
        name="字典数据编辑",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=5,
        icon="",
        perm="sys:dict-data:edit",
    )
    menu69 = SysMenu(
        id=140,
        parent_id=135,
        tree_path="0,1,135",
        name="字典数据删除",
        type=MenuType.BUTTON,
        route_name=None,
        route_path="",
        component=None,
        visible=1,
        sort=6,
        icon="",
        perm="sys:dict-data:delete",
    )

    # menu70 = SysMenu(
    #     id="6bc58e7c-b1b3-4aa9-b324-526a67c3d7a8",
    #     parent_id="06c49131-591a-4e82-9749-803f938911f2",
    #     tree_path="0,6bc58e7c-b1b3-4aa9-b324-526a67c3d7a8",
    #     name="模型管理",
    #     type=MenuType.MENU,
    #     route_name="Assets-3d",
    #     route_path="assets-3d",
    #     component="3D/model3d/index",
    #     visible=1,
    #     sort=1,
    #     icon="el-icon-Money",
    #     perm="3d:model:list",
    # )
    # menu71 = SysMenu(
    #     id="06c49131-591a-4e82-9749-803f938911f2",
    #     parent_id="0",
    #     tree_path="0",
    #     name="3D资产",
    #     type=MenuType.CATALOG,
    #     route_name=None,
    #     route_path="/assets_3d",
    #     component="Layout",
    #     visible=1,
    #     sort=2,
    #     icon="el-icon-Box",
    #     perm="3d:model",
    # )
    menu72 = SysMenu(
        id=300,
        parent_id=0,
        tree_path="0",
        name="上传管理",
        type=MenuType.CATALOG,
        route_name=None,
        route_path="/upload",
        component="Layout",
        visible=1,
        sort=2,
        icon="el-icon-Upload",
        perm="3d:upload",
    )
    menu73 = SysMenu(
        id=301,
        parent_id=300,
        tree_path="0,300",
        name="视频管理",
        type=MenuType.MENU,
        route_name="Video",
        route_path="/video",
        component="upload/video/index",
        visible=1,
        sort=1,
        icon="el-icon-VideoCamera",
        perm="3d:upload:video",
    )
    menu74 = SysMenu(
        id=302,
        parent_id=300,
        tree_path="0,300",
        name="图片管理",
        type=MenuType.MENU,
        route_name="Image",
        route_path="/image",
        component="upload/image/index",
        visible=1,
        sort=1,
        icon="el-icon-Picture",
        perm="3d:upload:image",
    )
    db.add_all(
        [
            menu1,
            menu2,
            menu3,
            menu4,
            menu5,
            menu6,
            menu7,
            menu8,
            menu9,
            menu10,
            menu11,
            menu12,
            menu13,
            menu14,
            menu15,
            menu16,
            menu17,
            menu18,
            menu19,
            menu20,
            menu21,
            menu22,
            menu23,
            menu24,
            menu25,
            menu26,
            menu27,
            menu28,
            menu29,
            menu30,
            menu31,
            menu32,
            menu33,
            menu34,
            menu35,
            menu36,
            menu37,
            menu38,
            menu39,
            menu40,
            menu41,
            menu42,
            menu43,
            menu44,
            menu45,
            menu46,
            menu47,
            menu48,
            menu49,
            menu50,
            menu51,
            menu52,
            menu53,
            menu54,
            menu55,
            menu56,
            menu57,
            menu58,
            menu59,
            menu60,
            menu61,
            menu62,
            menu63,
            menu64,
            menu65,
            menu66,
            menu67,
            menu68,
            menu69,
            menu72,
            menu73,
            menu74,
        ]
    )


def create_sys_dict_data(db: AsyncSession):
    sys_dict_data1 = SysDictItem(
        id=1, dict_code="gender", value="1", label="男", tag_type="primary", sort=1
    )
    sys_dict_data2 = SysDictItem(
        id=2, dict_code="gender", value="2", label="女", tag_type="danger", sort=2
    )
    sys_dict_data3 = SysDictItem(
        id=3, dict_code="gender", value="0", label="保密", tag_type="info", sort=3
    )
    sys_dict_data4 = SysDictItem(
        id=4,
        dict_code="notice_type",
        value="1",
        label="系统升级",
        tag_type="success",
        sort=1,
    )
    sys_dict_data5 = SysDictItem(
        id=5,
        dict_code="notice_type",
        value="2",
        label="系统维护",
        tag_type="primary",
        sort=2,
    )
    sys_dict_data6 = SysDictItem(
        id=6,
        dict_code="notice_type",
        value="3",
        label="安全警告",
        tag_type="danger",
        sort=3,
    )
    sys_dict_data7 = SysDictItem(
        id=7,
        dict_code="notice_type",
        value="4",
        label="假期通知",
        tag_type="success",
        sort=4,
    )
    sys_dict_data8 = SysDictItem(
        id=8,
        dict_code="notice_type",
        value="5",
        label="公司新闻",
        tag_type="primary",
        sort=5,
    )
    sys_dict_data9 = SysDictItem(
        id=9,
        dict_code="notice_type",
        value="99",
        label="其他",
        tag_type="info",
        sort=99,
    )
    sys_dict_data10 = SysDictItem(
        id=10,
        dict_code="notice_level",
        value="L",
        label="低",
        tag_type="info",
        sort=1,
    )
    sys_dict_data11 = SysDictItem(
        id=11,
        dict_code="notice_level",
        value="M",
        label="中",
        tag_type="warning",
        sort=2,
    )
    sys_dict_data12 = SysDictItem(
        id=12,
        dict_code="notice_level",
        value="H",
        label="高",
        tag_type="danger",
        sort=3,
    )
    db.add_all(
        [
            sys_dict_data1,
            sys_dict_data2,
            sys_dict_data3,
            sys_dict_data4,
            sys_dict_data5,
            sys_dict_data6,
            sys_dict_data7,
            sys_dict_data8,
            sys_dict_data9,
            sys_dict_data10,
            sys_dict_data11,
            sys_dict_data12,
        ]
    )


def create_sys_dict(db: AsyncSession):
    sys_dict1 = SysDict(id=1, code="gender", name="性别", status=1)
    sys_dict2 = SysDict(id=2, code="notice_type", name="通知类型", status=1)
    sys_dict3 = SysDict(id=3, code="notice_level", name="通知级别", status=1)
    db.add_all([sys_dict1, sys_dict2, sys_dict3])


def create_sys_dept(db: AsyncSession):
    sys_dept1 = SysDept(
        id=1, name="技术部", code="YOULAI", parent_id=0, tree_path="0", sort=0
    )

    sys_dept2 = SysDept(
        id=2, name="研发部门", code="RD001", parent_id=1, tree_path="0,1", sort=0
    )

    sys_dept3 = SysDept(
        id=3, name="测试部门", code="QA001", parent_id=1, tree_path="0,1", sort=0
    )
    db.add_all([sys_dept1, sys_dept2, sys_dept3])


if __name__ == "__main__":
    asyncio.run(create_initial_data())
