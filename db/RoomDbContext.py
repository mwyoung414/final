from BaseModels.BaseDbContext import *
from models.Room import Room

Base = declarative_base()
class RoomDb:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        
    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    async def GetAllRooms(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Room))
                return result.scalars().all()
            
    async def GetRoomPrice(self, room_type):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Room).where(Room.TYPE == room_type))
                return result.scalars().all()
            
    async def GetRoomById(self, room_id):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Room).where(Room.ID == room_id))
                return result.scalars().all()