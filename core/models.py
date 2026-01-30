from sqlalchemy import DateTime, Column, Integer, Text
from sqlalchemy.sql import func
from .database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    amount = Column(Integer, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"Payment(id={self.id}), {self.amount} {self.description}"
    
print(func)