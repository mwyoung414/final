from quart import jsonify
from models.models import User
from BaseModels.BaseDbContext import *
from sqlalchemy import String, Integer, Text, create_engine, inspect, func
import pandas as pd
from models.Hotels import Hotel
import os



Base = declarative_base()   
current_dir = os.path.dirname(os.path.abspath(__file__))
# Build path to the parquet file in the same directory
parquet_path = os.path.join(current_dir, "usa_hotels.parquet")
usa_hotels = pd.read_parquet(parquet_path)

print("original column names:", usa_hotels.columns.tolist())

usa_hotels.columns = [col.upper() for col in usa_hotels.columns]
print("modified column names:", usa_hotels.columns.tolist())

usa_hotels['HOTELNAME'] = usa_hotels['HOTELNAME'].astype(str)
usa_hotels['HOTELRATING'] = usa_hotels['HOTELRATING'].astype(int)
usa_hotels['ADDRESS'] = usa_hotels['ADDRESS'].astype(str)
usa_hotels['CITY'] = usa_hotels['CITY'].astype(str)
usa_hotels['STATE'] = usa_hotels['STATE'].astype(str)
usa_hotels['DESCRIPTION'] = usa_hotels['DESCRIPTION'].astype(str)



class HotelsDb:
    def __init__(self, db_url_async, db_url_sync):
        
        self.sync_engine = create_engine(db_url_sync, echo=True)
        
        self.async_engine = create_async_engine(db_url_async, echo=True)
        
        inspector = inspect(self.sync_engine)
        table_exists = 'hotels' in inspector.get_table_names()
        
        if not table_exists:
            usa_hotels.to_sql(
                "hotels",
                con=self.sync_engine,
                if_exists="replace",
                index=False,
                dtype={
                    "HOTELNAME": String(255),
                    "HOTELRATING": Integer(),
                    "ADDRESS": String(255),
                    "CITY": String(100),
                    "STATE": String(2),
                    "DESCRIPTION": Text()
                }
            )
        self.session = sessionmaker(bind = self.async_engine, class_=AsyncSession, expire_on_commit=False)
        
    async def init_db(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    async def addHotel(self, hotel):
        async with self.session() as session:
            async with session.begin():
                session.add(hotel)
            await session.commit()
        
        return jsonify({
            "message": "Hotel added successfully",
            "hotel": {
                "hotelname": hotel.hotelname,
                "hotelrating": hotel.hotelrating,
                "address": hotel.address,
                "city": hotel.city,
                "state": hotel.state,
                "hoteldesc": hotel.hoteldesc
            }
        }), 200
        
    async def getPagedHotels(self, page=1, per_page=9):
        """Get a specific page of hotels with the given page size"""
        offset = (page - 1) * per_page
        async with self.session() as session:
            result = await session.execute(
                select(Hotel)
                .order_by(Hotel.ID)  # Or any other ordering you prefer
                .offset(offset)
                .limit(per_page)
            )
            hotels = result.scalars().all()
            
            # Also get total count for pagination controls
            count_result = await session.execute(select(func.count(Hotel.ID)))
            total_count = count_result.scalar()
            
        return {
            "hotels": hotels,
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "pages": (total_count + per_page - 1) // per_page  # Ceiling division for total pages
        }
        
    async def getAllHotels(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Hotel))
                hotels = result.scalars().all()
        return hotels
    
    async def getHotelById(self, hotel_id):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Hotel).where(Hotel.ID == hotel_id))
                hotel = result.scalars().first()
        return hotel

