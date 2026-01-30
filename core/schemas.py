from pydantic import BaseModel, Field, field_validator, field_serializer
import re

class BasePaymentSchema(BaseModel):
    amount: float = Field()


class PaymentResponseSchema(BaseModel):
    amount: float = Field()
    id: int = Field()
    description: str = Field()
     
    @field_serializer('amount')
    def amount_serializer(cls, value):
        return round(value, 2)


class PaymentCreateSchema(BasePaymentSchema):
    description: str = Field()

    @field_validator("amount")
    def amount_validator(cls, value):
        if value >= 9999999.99:
            raise ValueError("amount cannot be larger than 10,000,000.00")
        return value

class PaymentReadSchema(BasePaymentSchema):
    id: int


class PaymentUpdateSchema(BasePaymentSchema):
    id: int
    description: str

