from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

# Postgres-side ceiling on any single statement. Without it a pathological query --
# e.g. the depth-N recursive CTE in fraud_graph.get_entity_neighbourhood, which has no
# cycle detection and so revisits nodes via back-edges -- holds its connection
# indefinitely and the awaiting HTTP request never returns. 30s is far above any
# legitimate query at demo scale, so this only ever fires on a runaway.
STATEMENT_TIMEOUT_MS = 30_000

engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
    connect_args={"server_settings": {"statement_timeout": str(STATEMENT_TIMEOUT_MS)}},
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
