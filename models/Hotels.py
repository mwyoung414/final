from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "HOTELS"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    HOTELNAME = Column(String(100), nullable=False)
    HOTELRATING = Column(Integer, nullable=False)
    ADDRESS = Column(String(255), nullable=False)
    CITY = Column(String(100), nullable=False)
    STATE = Column(String(2), ForeignKey("STATES.state_code"), nullable=False)
    DESCRIPTION = Column(String(65535), nullable=True)
