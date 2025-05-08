from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *


Base = declarative_base()

class Room(Base):
    __tablename__ = 'ROOMS'
    
    ID = Column(Integer, primary_key=True)
    TYPE = Column(Enum('QUEEN', 'KING', 'STUDIO', 'PENTHOUSE'), nullable=False)
    PRICE = Column(Integer, nullable=False)