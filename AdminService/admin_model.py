from BaseModels.BaseModel import *

# Define the base class

# Define the Admin model
class Admin(Base):
    __tablename__ = 'ADMINS'  # Name of the table in the database

    ID = Column(Integer, primary_key=True, autoincrement=True)
    FIRST_NAME = Column(String(50), nullable=False)
    LAST_NAME = Column(String(50), nullable=False)
    PHONE = Column(String(15), nullable=False)
    USERNAME = Column(String(50), nullable=False, unique=True)
    EMAIL = Column(String(100), nullable=False, unique=True)
    HASH = Column(String(128), nullable=False)
    SALT = Column(String(128), nullable=False)
    CREATED_AT = Column(DateTime, default=datetime.now().astimezone())
    UPDATED_AT = Column(DateTime, default=datetime.now().astimezone(), onupdate=datetime.now().astimezone())
    
    