import asyncio
import importlib
import logging
import sys

from app.core.database import AsyncSessionLocal, engine
from app.core.seeder import get_registered_seeders

import app.modules.users.models
import app.modules.roles.models

import app.modules.roles.seeder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_seeder(target: str | None = None) -> None:
    seeders = get_registered_seeders()
    seeders_sorted = sorted(seeders, key=lambda s: s.order)

    if target:
        seeders_sorted = [s for s in seeders_sorted if s.__name__ == target]
        if not seeders_sorted:
            logger.error(f"Seeder '{target}' not found.")
            return

    async with AsyncSessionLocal() as session:
        for SeederClass in seeders_sorted:
            logger.info(f"Running {SeederClass.__name__}...")
            seeder = SeederClass(session)
            try:
                await seeder.run()
                logger.info(f"{SeederClass.__name__} success.")
            except Exception as e:
                logger.error(f"{SeederClass.__name__} failed: {e}")
                await session.rollback()
                raise
    await engine.dispose()

if __name__ == "__main__":
    target_seeder = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(run_seeder(target=target_seeder))
