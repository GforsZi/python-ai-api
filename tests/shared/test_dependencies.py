import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from app.shared.dependencies import get_current_user

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    with patch("app.shared.dependencies.decode_access_token", return_value=None):
        dependency = get_current_user()
        with pytest.raises(HTTPException) as exc:
            await dependency(token="invalid", db=AsyncMock())
        assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_not_found():
    with patch("app.shared.dependencies.decode_access_token", return_value={"sub": "1"}):
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        dependency = get_current_user()
        with pytest.raises(HTTPException) as exc:
            await dependency(token="valid", db=mock_db)
        assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_current_user_success():
    mock_user = MagicMock(id=1, username="testuser", role_name="admin")
    with patch("app.shared.dependencies.decode_access_token", return_value={"sub": "1"}):
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.one_or_none.return_value = mock_user
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        dependency = get_current_user()
        user = await dependency(token="valid", db=mock_db)
        assert user.username == "testuser"

@pytest.mark.asyncio
async def test_get_current_user_forbidden_role():
    mock_user = MagicMock(id=1, username="testuser", role_name="user")
    with patch("app.shared.dependencies.decode_access_token", return_value={"sub": "1"}):
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.one_or_none.return_value = mock_user
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        dependency = get_current_user(allowed_roles=["admin"])
        with pytest.raises(HTTPException) as exc:
            await dependency(token="valid", db=mock_db)
        assert exc.value.status_code == 403
