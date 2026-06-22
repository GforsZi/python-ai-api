import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.seeds import run_seeder
from app.core.seeder import BaseSeeder

# Mock Seeder classes
class SeederA(BaseSeeder):
    order = 10
    async def run(self): pass

class SeederB(BaseSeeder):
    order = 5
    async def run(self): pass

@pytest.mark.asyncio
async def test_run_seeder_execution_order():
    mock_engine = AsyncMock()
    run_order = []
    
    async def run_a(self): run_order.append("SeederA")
    async def run_b(self): run_order.append("SeederB")
    
    with patch("app.seeds.get_registered_seeders", return_value=[SeederA, SeederB]), \
         patch("app.seeds.AsyncSessionLocal", new_callable=MagicMock) as mock_session_local, \
         patch("app.seeds.engine", new=mock_engine), \
         patch.object(SeederA, 'run', run_a), \
         patch.object(SeederB, 'run', run_b):
        
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        
        await run_seeder()
        
        assert run_order == ["SeederB", "SeederA"]
        assert mock_engine.dispose.called

@pytest.mark.asyncio
async def test_run_seeder_rollback_on_error():
    class FailingSeeder(BaseSeeder):
        async def run(self): raise Exception("Boom!")

    with patch("app.seeds.get_registered_seeders", return_value=[FailingSeeder]), \
         patch("app.seeds.AsyncSessionLocal", new_callable=MagicMock) as mock_session_local:
        
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        
        with pytest.raises(Exception, match="Boom!"):
            await run_seeder()
            
        assert mock_session.rollback.called

@pytest.mark.asyncio
async def test_run_seeder_target_filtering():
    with patch("app.seeds.get_registered_seeders", return_value=[SeederA, SeederB]), \
         patch("app.seeds.AsyncSessionLocal", new_callable=MagicMock) as mock_session_local, \
         patch.object(SeederA, 'run', new_callable=AsyncMock) as mock_run_a, \
         patch.object(SeederB, 'run', new_callable=AsyncMock) as mock_run_b:
        
        await run_seeder(target="SeederA")
        
        assert mock_run_a.called
        assert not mock_run_b.called
