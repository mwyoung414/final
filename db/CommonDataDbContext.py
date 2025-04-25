from models.models import STATES
from BaseModels.BaseDbContext import *

Base = declarative_base()

class CommonDataDb:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        
    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
            
    async def get_all_states(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(STATES))
                return result.scalars().all()



