import pytest
from unittest.mock import AsyncMock, patch
from app.core.database import get_db

@pytest.mark.asyncio
async def test_get_db_generator():
    # Mocking the session factory
    mock_session = AsyncMock()
    # AsyncSessionLocal() should return an asynchronous context manager
    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_session
    
    with patch("app.core.database.AsyncSessionLocal", return_value=mock_context_manager):
        # get_db is an async generator
        gen = get_db()
        
        # Start the generator
        session = await gen.__anext__()
        
        # Verify session is the mocked one
        assert session == mock_session
        
        # Clean up the generator
        try:
            await gen.__anext__()
        except StopAsyncIteration:
            pass
            
        # Verify session close is called
        assert mock_session.close.called
