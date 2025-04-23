from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *

Base = declarative_base()

class Customer(Base):
    __tablename__ = "CUSTOMERS"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    FIRSTNAME = Column(String(50), nullable=False)
    LASTNAME = Column(String(50), nullable=False)
    EMAIL = Column(String(100), nullable=False, unique=True)
    PHONE = Column(String(15), nullable=False, unique=True)
    ADDRESS = Column(String(255), nullable=False)
    CITY = Column(String(50), nullable=False)
    STATE = relationship("State", back_populates="States")
    ZIPCODE = Column(String(10), nullable=False)
    DATE_CREATED = Column(TIMESTAMP, server_default=func.now())
    LAST_UPDATED = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
