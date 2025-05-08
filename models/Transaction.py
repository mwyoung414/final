from BaseModels.BaseDbContext import *
from BaseModels.BaseModel import *
from sqlalchemy.orm import backref
from sqlalchemy import Numeric

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "TRANSACTION"
    
    ID = Column(Integer, autoincrement=True, primary_key=True)
    CUSTOMER_ID = Column(Integer, ForeignKey('USERS.ID'), nullable=False)
    BOOKING_ID = Column(Integer, ForeignKey('BOOKINGS.ID'), nullable=False)
    PAYMENT_ID = Column(Integer, ForeignKey('PAYMENT.ID'), nullable=True)
    
    TRANSACTION_NUMBER = Column(String(20), nullable=False, unique=True)
    AMOUNT = Column(Numeric(10, 2), nullable=False)
    CURRENCY = Column(String(3), default='USD', nullable=False)
    
    customer = relationship("User", backref=backref("transactions", lazy="dynamic"))
    booking = relationship("Booking", backref=backref("transactions", lazy="dynamic"))
    payment = relationship("Payment", backref=backref("transactions", lazy="dynamic"))