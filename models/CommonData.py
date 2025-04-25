from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *

Base = declarative_base()

class STATES(Base):
    __tablename__ = 'STATES'
    state_code = Column(String(2), primary_key=True)
    