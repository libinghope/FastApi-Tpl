import pytest
from unittest.mock import MagicMock, AsyncMock
from app.main import app
from app.api import deps
from app.models.sys.dept import SysDept
from app.models.sys.user import SysUser

# Mock User
mock_user = SysUser(
    id=1,
    username="admin",
    nickname="Administrator",
    email="admin@example.com",
    is_active=True,
    is_superuser=True,
    gender=1,
)

@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalar_one_or_none.return_value = None
    mock_result.scalar.return_value = None
    session.execute.return_value = mock_result
    session.get.return_value = None
    session.add = MagicMock()
    return session

@pytest.fixture
def override_deps(mock_db_session):
    async def override_get_db():
        yield mock_db_session

    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[deps.get_db] = override_get_db
    app.dependency_overrides[deps.get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}

@pytest.mark.anyio
async def test_dept_tree(client, override_deps, mock_db_session):
    # Prepare data
    depts = [
        SysDept(id=1, name="Root", code="root", parent_id=0, sort=1, status=1, tree_path="0"),
        SysDept(id=2, name="Child", code="child", parent_id=1, sort=1, status=1, tree_path="0,1"),
    ]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = depts
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/admin/sys/dept/tree")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Root"
    assert len(data[0]["children"]) == 1
    assert data[0]["children"][0]["name"] == "Child"

@pytest.mark.anyio
async def test_add_dept(client, override_deps, mock_db_session):
    payload = {
        "name": "New Dept",
        "code": "new_dept",
        "parent_id": 0,
        "sort": 1,
        "status": 1
    }
    mock_db_session.scalar.return_value = None # Code check: not found

    response = await client.post("/api/v1/admin/sys/dept/add", json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 200

@pytest.mark.anyio
async def test_add_dept_duplicate(client, override_deps, mock_db_session):
    payload = {"name": "Dup", "code": "dup", "parent_id": 0}
    mock_db_session.scalar.return_value = SysDept(id=1, code="dup") # Found

    response = await client.post("/api/v1/admin/sys/dept/add", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.anyio
async def test_update_dept(client, override_deps, mock_db_session):
    payload = {
        "id": 2,
        "name": "Updated",
        "code": "child",
        "parent_id": 1,
        "sort": 2,
        "status": 1
    }
    dept = SysDept(id=2, name="Child", code="child", parent_id=1, tree_path="0,1")
    mock_db_session.get.return_value = dept
    # Mock parent lookup if parent changed (not changed here)
    
    response = await client.put("/api/v1/admin/sys/dept/update", json=payload)
    assert response.status_code == 200
    assert dept.name == "Updated"

@pytest.mark.anyio
async def test_delete_dept(client, override_deps, mock_db_session):
    payload = {"ids": [2]}
    # Mock checks
    mock_db_session.scalar.return_value = None # No children, no users
    
    response = await client.post("/api/v1/admin/sys/dept/delete", json=payload)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_delete_dept_with_children(client, override_deps, mock_db_session):
    payload = {"ids": [1]}
    # Mock checks
    mock_db_session.scalar.side_effect = [True, False] # Has children, no users
    
    response = await client.post("/api/v1/admin/sys/dept/delete", json=payload)
    assert response.status_code == 400
    assert "children" in response.json()["detail"]
