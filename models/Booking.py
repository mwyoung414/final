from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *

Base = declarative_base()

class Booking(Base):
    __tablename__ = 'BOOKINGS'
    
    ID = Column(Integer, primary_key=True)
    ORDER_NUMBER = Column(String(12), nullable=False, unique=True)
    USER_ID = Column(Integer, ForeignKey('USERS.ID'), nullable=False)
    ROOM_ID = Column(Integer, ForeignKey('ROOMS.ID'), nullable=False)
    NUM_OF_ROOMS = Column(Integer, nullable=False)
    CHECK_IN_DATE = Column(DateTime, nullable=False)
    CHECK_OUT_DATE = Column(DateTime, nullable=False)
    TOTAL_NIGHTS = Column(Integer, nullable=False)
    TOTAL_PRICE = Column(Integer, nullable=False)
    DATE_CREATED = Column(TIMESTAMP, server_default=func.now())
    LAST_UPDATED = Column(TIMESTAMP, default=func.now(), onupdate=func.now())