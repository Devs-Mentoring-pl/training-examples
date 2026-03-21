from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cykl życia aplikacji – setup i teardown."""
    # Startup – tworzenie tabel (tylko do prototypowania!)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown – tu można zamknąć połączenia, wyczyścić cache itp.
    await engine.dispose()


app = FastAPI(title="Task Manager API", lifespan=lifespan)

app.include_router(users.router)
app.include_router(tasks.router)
