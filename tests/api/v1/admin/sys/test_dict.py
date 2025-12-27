import pytest
from unittest.mock import MagicMock, AsyncMock
from app.main import app
from app.api import deps
from app.models.sys.user import SysUser
from app.models.sys.dictionary import SysDict, SysDictItem

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
        return mock_user

    app.dependency_overrides[deps.get_db] = override_get_db
    app.dependency_overrides[deps.get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}

@pytest.mark.anyio
async def test_list_dicts(client, override_deps, mock_db_session):
    # Mock data
    dict_list = [
        SysDict(id=1, code="gender", name="Gender", status=1, sort=1),
        SysDict(id=2, code="status", name="Status", status=1, sort=2),
    ]
    
    # Mock execute side effect for different queries
    async def side_effect_execute(stmt):
        str_stmt = str(stmt).lower()
        m = MagicMock()
        if "count" in str_stmt:
            m.scalar.return_value = 2
            return m
        elif "sys_dict" in str_stmt:
            m.scalars.return_value.all.return_value = dict_list
            return m
        m.scalars.return_value.all.return_value = []
        return m

    mock_db_session.execute.side_effect = side_effect_execute
    mock_db_session.scalar.return_value = 2

    response = await client.get("/api/v1/admin/sys/dict/list")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["list"]) == 2
    assert data["list"][0]["code"] == "gender"

@pytest.mark.anyio
async def test_add_dict(client, override_deps, mock_db_session):
    payload = {
        "code": "new_type",
        "name": "New Type",
        "status": 1,
        "sort": 10
    }
    
    # Mock checks (not exists)
    mock_db_session.scalar.return_value = None
    
    response = await client.post("/api/v1/admin/sys/dict/add", json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 200

@pytest.mark.anyio
async def test_update_dict(client, override_deps, mock_db_session):
    payload = {
        "id": 1,
        "code": "updated_type",
        "name": "Updated Type"
    }
    
    mock_obj = SysDict(id=1, code="old", name="Old")
    mock_db_session.get.return_value = mock_obj
    
    response = await client.post("/api/v1/admin/sys/dict/update", json=payload)
    assert response.status_code == 200
    assert mock_obj.name == "Updated Type"

@pytest.mark.anyio
async def test_delete_dict(client, override_deps, mock_db_session):
    payload = {"uid_arr": [1, 2]}
    response = await client.post("/api/v1/admin/sys/dict/delete", json=payload)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_list_dict_items(client, override_deps, mock_db_session):
    items = [
        SysDictItem(id=1, dict_code="gender", label="Male", value="1", status=1, sort=1),
        SysDictItem(id=2, dict_code="gender", label="Female", value="2", status=1, sort=2),
    ]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = items
    mock_db_session.execute.return_value = mock_result
    
    response = await client.get("/api/v1/admin/sys/dict/items/gender/list")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["label"] == "Male"

@pytest.mark.anyio
async def test_add_dict_item(client, override_deps, mock_db_session):
    payload = {
        "dict_code": "gender",
        "label": "Unknown",
        "value": "3",
        "sort": 3,
        "status": 1
    }
    
    response = await client.post("/api/v1/admin/sys/dict/items/add", json=payload)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_update_dict_item(client, override_deps, mock_db_session):
    payload = {
        "id": 1,
        "dict_code": "gender",
        "label": "Male Updated",
        "value": "1",
        "sort": 1,
        "status": 1
    }
    
    mock_item = SysDictItem(id=1, label="Male")
    mock_db_session.get.return_value = mock_item
    
    response = await client.post("/api/v1/admin/sys/dict/items/update", json=payload)
    assert response.status_code == 200
    assert mock_item.label == "Male Updated"

@pytest.mark.anyio
async def test_delete_dict_item(client, override_deps, mock_db_session):
    payload = {"uid_arr": [1]}
    response = await client.post("/api/v1/admin/sys/dict/items/delete", json=payload)
    assert response.status_code == 200
