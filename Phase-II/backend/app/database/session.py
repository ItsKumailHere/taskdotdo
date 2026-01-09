import ssl
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings


# Create async engine
DATABASE_URL = settings.DATABASE_URL

# Configure SSL context for Neon connections
ssl_context = ssl.create_default_context()

async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"ssl": ssl_context},
    pool_pre_ping=True,  # Verify connections before using (good for Neon)
    pool_size=5,         # Limit connection pool (good for Neon Serverless)
    max_overflow=10,
    pool_recycle=300,    # Recycle connections after 5 minutes
)


# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


# Dependency for FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session