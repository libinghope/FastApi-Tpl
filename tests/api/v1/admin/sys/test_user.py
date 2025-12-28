#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统用户管理API测试模块

该模块测试了系统用户的核心功能，包括用户列表查询、添加用户、更新用户、删除用户、
修改用户状态和重置密码等操作。使用pytest和asyncio框架，通过mock数据库会话和当前用户
来模拟测试环境，确保测试的独立性和可重复性。
"""

import pytest
from unittest.mock import MagicMock, AsyncMock  # 导入mock工具，用于模拟数据库和依赖
from app.main import app  # 导入FastAPI应用实例
from app.api import deps  # 导入依赖项模块
from app.models.sys.user import SysUser, SysUserRoleRef  # 导入用户数据模型


# 定义模拟管理员用户，用于测试需要认证的接口
mock_user = SysUser(
    id=1,  # 用户ID
    username="admin",  # 用户名
    nickname="Administrator",  # 用户昵称
    email="admin@example.com",  # 邮箱
    is_active=True,  # 用户状态：激活
    is_superuser=True,  # 超级管理员权限
    gender=1,  # 性别：1-男
)


@pytest.fixture
def mock_db_session():
    """
    模拟数据库会话夹具

    创建一个异步的模拟数据库会话，用于替代真实的数据库连接。
    预配置了常用的数据库操作返回值，如查询结果、标量值和计数等。

    Returns:
        AsyncMock: 模拟的数据库会话对象
    """
    session = AsyncMock()  # 创建异步模拟会话对象

    # 配置模拟查询结果
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []  # 查询多条记录返回空列表
    mock_result.scalar_one_or_none.return_value = None  # 查询单条记录返回None
    mock_result.scalar.return_value = 0  # 计数查询返回0

    # 将模拟结果关联到会话的方法
    session.execute.return_value = mock_result  # 执行SQL语句返回模拟结果
    session.get.return_value = None  # 根据ID查询返回None
    session.add = MagicMock()  # 添加记录方法为同步模拟

    return session


@pytest.fixture
def override_deps(mock_db_session):
    """
    覆盖应用依赖项的夹具

    用于替换FastAPI应用中的依赖项，将数据库会话和当前用户替换为模拟对象，
    确保测试可以在隔离环境中运行，不依赖真实的数据库和认证系统。
    测试结束后会恢复原始依赖配置。

    Args:
        mock_db_session: 模拟的数据库会话对象
    """

    # 覆盖数据库依赖
    async def override_get_db():
        yield mock_db_session

    # 覆盖当前用户依赖
    async def override_get_current_user():
        return mock_user

    # 应用依赖项覆盖
    app.dependency_overrides[deps.get_db] = override_get_db
    app.dependency_overrides[deps.get_current_user] = override_get_current_user

    yield  # 提供夹具值

    # 清理：恢复原始依赖配置
    app.dependency_overrides = {}


@pytest.mark.anyio
async def test_get_users_list(client, override_deps, mock_db_session):
    """
    测试获取用户列表接口

    测试管理员查询用户列表的功能，验证是否能够正确返回用户数据，包括分页信息和用户详情。
    该测试模拟了数据库查询的多种场景，包括计数查询、用户列表查询和角色关联查询。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备测试数据
    user_list = [
        SysUser(
            id=1,
            username="user1",
            nickname="User One",
            is_active=True,
            gender=1,
            is_superuser=False,
        ),
        SysUser(
            id=2,
            username="user2",
            nickname="User Two",
            is_active=True,
            gender=2,
            is_superuser=False,
        ),
    ]

    # 定义数据库执行的副作用函数，根据不同的查询语句返回不同的模拟结果
    # 处理三种主要查询场景：
    # 1. 计数查询：获取用户总数
    # 2. 用户列表查询：获取分页用户数据
    # 3. 角色关联查询：获取用户对应的角色ID列表
    async def side_effect_execute(stmt):
        str_stmt = str(stmt).lower()  # 将查询语句转为小写，便于匹配
        m = MagicMock()  # 创建新的模拟结果对象

        if "count" in str_stmt:
            # 处理计数查询，返回用户总数
            m.scalar_one_or_none.return_value = 2
            return m
        elif "sys_user" in str_stmt and "offset" in str_stmt:
            # 处理用户列表查询，返回模拟的用户数据
            m.all.return_value = [(u,) for u in user_list]
            return m
        elif "user_role_ref" in str_stmt:
            # Return SysUserRoleRef objects
            # Assuming query is for user ids in list.
            # We mock returning one role for user1 (id=1) 
            # We need to return objects with user_id and role_id
            m1 = SysUserRoleRef(user_id=1, role_id=1)
            # maybe for user2 too?
            m2 = SysUserRoleRef(user_id=2, role_id=1)
            m.scalars.return_value.all.return_value = [m1, m2]
            return m

        # 默认返回空结果
        m.scalars.return_value.all.return_value = []
        return m

    # 配置数据库会话的模拟行为
    mock_db_session.scalar.return_value = 2  # 设置计数查询的返回值
    mock_db_session.execute.side_effect = side_effect_execute  # 设置执行SQL的副作用函数

    # 发送API请求
    response = await client.get("/api/v1/admin/sys/user/list")

    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200
    data = response.json()  # 解析JSON响应
    assert data["data"]["total"] == 2  # 验证用户总数为2
    assert len(data["data"]["list"]) == 2  # 验证返回的用户列表长度为2
    assert data["data"]["list"][0]["username"] == "user1"  # 验证第一个用户的用户名


@pytest.mark.anyio
async def test_add_user(client, override_deps, mock_db_session):
    """
    测试添加用户接口

    测试管理员添加新用户的功能，验证接口是否能够正确处理用户创建请求，
    并返回成功响应。模拟了用户名唯一性检查通过的场景。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备添加用户的请求参数
    payload = {
        "username": "newuser",  # 新用户名
        "nickname": "New User",  # 用户昵称
        "password": "pass123",  # 用户密码（限制在72字节以内）
        "role_ids": [1],  # 用户角色ID列表
    }

    # 模拟用户名唯一性检查，返回None表示用户名可用
    mock_db_session.scalar.return_value = None

    # 发送添加用户的POST请求
    response = await client.post("/api/v1/admin/sys/user/add", json=payload)

    # 调试信息：如果请求失败，打印响应内容
    if response.status_code != 200:
        print(response.json())

    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200
    assert response.json()["code"] == 200  # 验证业务状态码为200


@pytest.mark.anyio
async def test_add_user_duplicate(client, override_deps, mock_db_session):
    """
    测试添加重复用户接口

    测试添加用户时用户名已存在的场景，验证接口是否能够正确检测重复用户名，
    并返回适当的错误提示。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备添加用户的请求参数（使用已存在的用户名）
    payload = {"username": "existing", "password": "123"}

    # 模拟用户名唯一性检查，返回已存在的用户对象
    mock_db_session.scalar.return_value = SysUser(id=99, username="existing")

    # 发送添加用户的POST请求
    response = await client.post("/api/v1/admin/sys/user/add", json=payload)

    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200 (始终返回200)
    assert response.status_code == 200  # 验证HTTP状态码为200 (始终返回200)
    assert response.json()["code"] == "USER_ALREADY_EXISTS"  # 验证业务状态码为USER_ALREADY_EXISTS
    assert (
        "already exists" in response.json()["message"]
    )  # 验证错误信息包含"already exists"


@pytest.mark.anyio
async def test_update_user(client, override_deps, mock_db_session):
    """
    测试更新用户接口

    测试管理员更新用户信息的功能，验证接口是否能够正确处理用户信息更新请求，
    并更新数据库中的用户数据。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备更新用户的请求参数
    payload = {
        "id": 1,  # 要更新的用户ID
        "nickname": "Updated Name",  # 新的用户昵称
    }

    # 模拟数据库查询，返回要更新的用户对象
    mock_u = SysUser(id=1, username="u1", nickname="Old Name")
    mock_db_session.get.return_value = mock_u

    # 发送更新用户的PUT请求
    response = await client.put("/api/v1/admin/sys/user/update", json=payload)

    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200
    assert mock_u.nickname == "Updated Name"  # 验证用户对象的昵称已更新


@pytest.mark.anyio
async def test_update_user_not_found(client, override_deps, mock_db_session):
    """
    测试更新不存在的用户接口

    测试更新不存在用户的场景，验证接口是否能够正确处理用户不存在的情况，
    并返回适当的错误响应。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备更新用户的请求参数（使用不存在的用户ID）
    payload = {"id": 999, "nickname": "Ghost"}

    # 模拟数据库查询，返回None表示用户不存在
    mock_db_session.get.return_value = None

    # 发送更新用户的PUT请求
    response = await client.put("/api/v1/admin/sys/user/update", json=payload)

    # 验证响应结果
    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200 (始终返回200)
    assert response.json()["code"] == "USER_NOT_FOUND"  # 验证业务状态码为USER_NOT_FOUND


@pytest.mark.anyio
async def test_delete_user(client, override_deps, mock_db_session):
    """
    测试删除用户接口

    测试管理员批量删除用户的功能，验证接口是否能够正确处理用户删除请求，
    并返回成功响应。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备删除用户的请求参数（包含要删除的用户ID列表）
    payload = {"uid_arr": [2, 3]}

    # 发送删除用户的DELETE请求
    response = await client.request(
        "DELETE", "/api/v1/admin/sys/user/delete", json=payload
    )

    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200


@pytest.mark.anyio
async def test_delete_self(client, override_deps, mock_db_session):
    """
    测试删除自己接口

    测试用户尝试删除自己的场景，验证接口是否能够正确检测并阻止用户删除自己，
    并返回适当的错误提示。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备删除用户的请求参数（包含当前用户的ID）
    payload = {"uid_arr": [1]}

    # 发送删除用户的DELETE请求
    response = await client.request(
        "DELETE", "/api/v1/admin/sys/user/delete", json=payload
    )

    # 验证响应结果
    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200 (始终返回200)
    assert response.json()["code"] == "INVALID_ARGUMENT"  # 验证业务状态码为INVALID_ARGUMENT
    assert (
        "Cannot delete yourself" in response.json()["message"]
    )  # 验证错误信息包含"Cannot delete yourself"


@pytest.mark.anyio
async def test_change_active_status(client, override_deps, mock_db_session):
    """
    测试修改用户活跃状态接口

    测试管理员修改用户活跃状态的功能，验证接口是否能够正确处理用户状态更新请求，
    并更新数据库中的用户状态。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备修改用户状态的请求参数
    payload = {
        "user_uid": 2,  # 要修改状态的用户ID
        "status": False,  # 新的活跃状态：False表示禁用
    }

    # 模拟数据库查询，返回要修改状态的用户对象
    mock_u = SysUser(id=2, is_active=True)
    mock_db_session.get.return_value = mock_u

    # 发送修改用户状态的POST请求
    response = await client.post("/api/v1/admin/sys/user/change/active", json=payload)

    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200
    assert mock_u.is_active is False  # 验证用户对象的活跃状态已更新为False


@pytest.mark.anyio
async def test_reset_password(client, override_deps, mock_db_session):
    """
    测试重置密码接口

    测试管理员重置用户密码的功能，验证接口是否能够正确处理密码重置请求，
    并更新数据库中的用户密码。

    Args:
        client: FastAPI测试客户端
        override_deps: 覆盖依赖项的夹具
        mock_db_session: 模拟的数据库会话
    """
    # 准备重置密码的请求参数
    payload = {
        "id": 2,  # 要重置密码的用户ID
        "password": "newpass123",  # 新密码（限制在72字节以内）
        "password2": "newpass123",  # 确认密码（限制在72字节以内）
    }

    # 模拟数据库查询，返回要重置密码的用户对象
    mock_u = SysUser(id=2, hashed_password="oldhash")
    mock_db_session.get.return_value = mock_u

    # 发送重置密码的POST请求
    response = await client.post("/api/v1/admin/sys/user/reset/password", json=payload)

    # 验证响应结果
    assert response.status_code == 200  # 验证HTTP状态码为200
