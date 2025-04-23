from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *

Base = declarative_base()

class State(Base):
    __tablename__ = "STATES"
    state_code = Column(String(2), nullable=False, unique=True, primary_key=True)
    