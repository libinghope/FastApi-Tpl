
import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
from app.main import app
from app.api import deps
from app.models.sys.config import SysConfig, ConfigTypeEnum
from app.models.sys.user import SysUser

# Mock user
mock_user = SysUser(
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
    mock_result.scalars.return_value.first.return_value = None
    mock_result.scalar.return_value = 0
    
    session.execute.return_value = mock_result
    session.get.return_value = None
    
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
async def test_get_config_list(client, override_deps, mock_db_session):
    # Setup
    now = datetime.now()
    config_list = [
        SysConfig(id=1, name="Cfg1", key="k1", value="v1", type=ConfigTypeEnum.STRING, create_time=now, update_time=now),
        SysConfig(id=2, name="Cfg2", key="k2", value="v2", type=ConfigTypeEnum.STRING, create_time=now, update_time=now)
    ]
    
    async def side_effect(stmt):
        str_stmt = str(stmt).lower()
        m = MagicMock()
        if "count" in str_stmt:
            # scalar is called for count
            pass 
        if "sys_config" in str_stmt:
            m.scalars.return_value.all.return_value = config_list
            return m
        return m
        
    mock_db_session.execute.side_effect = side_effect
    mock_db_session.scalar.return_value = 2
    
    resp = await client.get("/api/v1/admin/sys/config/list")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["list"]) == 2

@pytest.mark.anyio
async def test_add_config(client, override_deps, mock_db_session):
    payload = {
        "name": "New Config",
        "key": "new.key",
        "value": "val",
        "type": "string"
    }
    # Mock duplicate check -> returns empty (None)
    mock_db_session.execute.return_value.scalars.return_value.first.return_value = None
    
    async def refresh_side_effect(obj):
        obj.id = 1
        obj.create_time = datetime.now()
        obj.update_time = datetime.now()
        
    mock_db_session.refresh.side_effect = refresh_side_effect
    
    resp = await client.post("/api/v1/admin/sys/config/add", json=payload)
    if resp.status_code != 200:
        print(resp.json())
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Config"

@pytest.mark.anyio
async def test_add_config_duplicate(client, override_deps, mock_db_session):
    payload = {
        "name": "Existing",
        "key": "exist.key",
        "value": "val",
        "type": "string"
    }
    # Mock duplicate check -> returns existing
    mock_db_session.execute.return_value.scalars.return_value.first.return_value = SysConfig(id=1, key="exist.key", name="Existing")
    
    resp = await client.post("/api/v1/admin/sys/config/add", json=payload)
    assert resp.status_code == 400
    assert "already exists" in resp.json()["detail"]

@pytest.mark.anyio
async def test_update_config(client, override_deps, mock_db_session):
    payload = {
        "id": 1,
        "name": "Updated",
        "key": "k1",
        "value": "v1",
        "type": "string"
    }
    now = datetime.now()
    mock_obj = SysConfig(id=1, name="Old", key="k1", type=ConfigTypeEnum.STRING, create_time=now, update_time=now)
    mock_db_session.get.return_value = mock_obj
    
    # Mock duplicate check -> returns None
    # We need access to the first call's return value which is for SELECT ... 
    # But get is a separate call.
    # The execute called inside update_config is for duplicate check.
    
    # db.execute is called.
    mock_db_session.execute.return_value.scalars.return_value.first.return_value = None
    
    async def refresh_side_effect(obj):
        pass # id exists
        
    mock_db_session.refresh.side_effect = refresh_side_effect

    resp = await client.post("/api/v1/admin/sys/config/update", json=payload)
    assert resp.status_code == 200
    assert mock_obj.name == "Updated"

@pytest.mark.anyio
async def test_delete_config(client, override_deps, mock_db_session):
    mock_obj = SysConfig(id=1, name="Del", key="del")
    mock_db_session.get.return_value = mock_obj
    
    resp = await client.request("DELETE", "/api/v1/admin/sys/config/delete/1")
    assert resp.status_code == 200
    assert mock_obj.delete_time is not None
