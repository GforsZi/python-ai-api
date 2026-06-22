import pytest
from app.core.seeder import BaseSeeder, register_seeder, get_registered_seeders
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch

# Bersihkan registri sebelum setiap test
@pytest.fixture(autouse=True)
def clear_registry():
    from app.core import seeder
    seeder._seeder_registry = []

def test_register_seeder():
    @register_seeder
    class MockSeeder(BaseSeeder):
        async def run(self):
            pass
    
    seeders = get_registered_seeders()
    assert len(seeders) == 1
    assert seeders[0] == MockSeeder

@pytest.mark.asyncio
async def test_base_seeder_logging():
    class MinimalSeeder(BaseSeeder):
        async def run(self):
            pass
            
    mock_session = AsyncMock(spec=AsyncSession)
    seeder = MinimalSeeder(session=mock_session)
    
    with patch("app.core.seeder.logger") as mock_logger:
        await seeder.log("test message")
        mock_logger.info.assert_called_with("[MinimalSeeder] test message")

def test_base_seeder_is_abstract():
    with pytest.raises(TypeError):
        BaseSeeder(session=AsyncMock())
