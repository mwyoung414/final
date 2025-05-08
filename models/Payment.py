from BaseModels.BaseModel import *
from BaseModels.BaseDbContext import *

Base = declarative_base()

class Payment(Base):
    __tablename__ = 'PAYMENT'
    
    ID = Column(Integer, autoincrement=True, primary_key=True)
    BOOKING_ID = Column(Integer, ForeignKey('BOOKINGS.ID'), nullable=False)
    PAYMENT_TOKEN = Column(String(64), nullable=False)  # Token from payment processor
    CARD_LAST_FOUR = Column(String(4), nullable=False)  # Last 4 digits only
    CARD_TYPE = Column(String(20), nullable=False)  # Visa, MasterCard, etc.
    CARD_HOLDER_NAME = Column(String(100), nullable=False)
    EXPIRY_MONTH = Column(String(2), nullable=False)
    EXPIRY_YEAR = Column(String(4), nullable=False)
    AMOUNT = Column(Numeric(10, 2), nullable=False)
    CURRENCY = Column(String(3), default='USD')
    STATUS = Column(String(20), nullable=False)  # 'completed', 'pending', 'failed'
    TRANSACTION_ID = Column(String(64))  # From payment processor
    CREATED_AT = Column(TIMESTAMP, server_default=func.now())