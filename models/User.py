from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *

Base = declarative_base()
class User(Base):
        __tablename__ = "USERS"
        ID = Column(Integer, primary_key=True, autoincrement=True)
        USERNAME = Column(String(50), nullable=False, unique=True)
        FIRSTNAME = Column(String(50), nullable=False)
        LASTNAME = Column(String(50), nullable=False)
        ADDRESS = Column(String(255), nullable=False)
        CITY = Column(String(50), nullable=False)
        STATE = Column(String(2), nullable=False)
        ZIPCODE = Column(String(10), nullable=False)
        EMAIL = Column(String(100), nullable=False, unique=True)
        ROLE = Column(Enum("USER", "ADMIN"), nullable=False)
        HASH = Column(String(255), nullable=False)
        SALT = Column(String(255), nullable=False)
        IS_ACTIVE = Column(Boolean, default=True)
        DATE_CREATED = Column(TIMESTAMP, server_default = func.now())
        LAST_UPDATED = Column(TIMESTAMP, default=func.now(), onupdate=func.now())