import pytest
from unittest.mock import MagicMock, AsyncMock
from app.main import app
from app.api import deps
from app.models.sys.role import SysRole
from app.models.sys.user import SysUser
from app.models.sys.menu import SysRoleMenu

# Mock User
mock_superuser = SysUser(
    id=1,
    username="admin",
    is_active=True,
    is_superuser=True
)

@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalar_one_or_none.return_value = None
    mock_result.scalar.return_value = 0
    
    session.execute.return_value = mock_result
    session.get.return_value = None
    session.add = MagicMock()
    
    return session

@pytest.fixture
def override_deps(mock_db_session):
    async def override_get_db():
        yield mock_db_session

    async def override_get_current_user():
        return mock_superuser

    app.dependency_overrides[deps.get_db] = override_get_db
    app.dependency_overrides[deps.get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}

@pytest.mark.anyio
async def test_role_list(client, override_deps, mock_db_session):
    roles = [
        SysRole(id=1, name="Admin", code="admin", status=1),
        SysRole(id=2, name="User", code="user", status=1)
    ]
    
    # Side effect for count and list
    async def side_effect_execute(stmt):
        str_stmt = str(stmt).lower()
        m = MagicMock()
        if "count" in str_stmt:
            # scalar() called for count
            m.scalars.return_value.all.return_value = [] # unused for scalar
            return m
        else:
            m.scalars.return_value.all.return_value = roles
            return m
            
    mock_db_session.execute.side_effect = side_effect_execute
    mock_db_session.scalar.return_value = 2 # for count
    
    response = await client.get("/api/v1/admin/sys/role/list")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["list"]) == 2
    assert data["list"][0]["name"] == "Admin"

@pytest.mark.anyio
async def test_add_role(client, override_deps, mock_db_session):
    payload = {
        "name": "New Role",
        "code": "new_role",
        "intro": "Description",
        "status": 1,
        "sort": 1
    }
    
    mock_db_session.scalar.return_value = None # duplicate check
    
    response = await client.post("/api/v1/admin/sys/role/add", json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 200

@pytest.mark.anyio
async def test_add_role_duplicate(client, override_deps, mock_db_session):
    payload = {"name": "Dup", "code": "dup"}
    mock_db_session.scalar.return_value = SysRole(id=1) 
    
    response = await client.post("/api/v1/admin/sys/role/add", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.anyio
async def test_update_role(client, override_deps, mock_db_session):
    payload = {
        "id": 1,
        "name": "Updated Role",
        "code": "admin"
    }
    role = SysRole(id=1, name="Admin", code="admin")
    mock_db_session.get.return_value = role
    
    response = await client.post("/api/v1/admin/sys/role/update", json=payload)
    assert response.status_code == 200
    assert role.name == "Updated Role"

@pytest.mark.anyio
async def test_delete_role(client, override_deps, mock_db_session):
    payload = {"ids": [1]}
    response = await client.post("/api/v1/admin/sys/role/delete", json=payload)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_assign_perms(client, override_deps, mock_db_session):
    role_id = 1
    payload = {"menu_ids": [1, 2, 3]}
    
    role = SysRole(id=1)
    mock_db_session.get.return_value = role
    
    response = await client.post(f"/api/v1/admin/sys/role/{role_id}/assign_perms", json=payload)
    assert response.status_code == 200
    
    # Verify deletions and insertions happened
    # Hard to verify exact SQL calls with simple mocks, checking success is first step.
    # We can check if `db.execute` was called.
    assert mock_db_session.execute.call_count >= 2 # 1 delete, 1 insert (if menu_ids present)

@pytest.mark.anyio
async def test_get_role_menu_ids(client, override_deps, mock_db_session):
    role_id = 1
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [10, 20]
    mock_db_session.execute.return_value = mock_result
    
    response = await client.get(f"/api/v1/admin/sys/role/{role_id}/menu_ids")
    assert response.status_code == 200
    assert response.json()["result"] == [10, 20]
