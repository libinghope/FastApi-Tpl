import asyncio
import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.db.init_db import init_db

async def main() -> None:
    print("Creating initial data...")
    async with SessionLocal() as session:
        await init_db(session)
    print("Initial data created.")

if __name__ == "__main__":
    asyncio.run(main())
