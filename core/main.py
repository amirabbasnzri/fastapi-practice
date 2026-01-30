from fastapi import FastAPI, status, HTTPException, Depends
from .database import engine, Base, get_session
from contextlib import asynccontextmanager
from typing import List
from sqlalchemy.orm import Session
from .schemas import (PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema,)
from .models import Payment

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is startup")
    Base.metadata.create_all(engine)
    yield
    print("Application is shutdown")

app = FastAPI(lifespan=lifespan)

@app.post("/payments/add", status_code=status.HTTP_201_CREATED, response_model=PaymentResponseSchema,)
def add_payment(request: PaymentCreateSchema, session: Session = Depends(get_session)):
    new_payment = Payment(description=request.description, amount=request.amount)
    session.add(new_payment)
    session.refresh(new_payment)
    return new_payment
    
@app.get("/payments", response_model=List[PaymentResponseSchema])
def see_payments(session: Session = Depends(get_session)):
    payments = session.query(Payment).all()
    return payments


@app.get("/payments/id/{id}", response_model=PaymentResponseSchema)
def see_item_by_id(id: int, session: Session = Depends(get_session)):
    obj = session.query(Payment).filter(Payment.id == id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id does not exist')
    return obj

@app.put("/payments/edit/{id}", response_model=PaymentResponseSchema)
def update_amount(id: int, request: PaymentUpdateSchema, session: Session = Depends(get_session)):
    payment = session.query(Payment).filter(Payment.id == id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id does not exist')
    payment.amount = request.amount
    payment.description = request.description
    session.refresh(payment)
    return payment


@app.delete("/payments/delete/{id}", response_model=PaymentResponseSchema)
def delete_item(id: int, session: Session = Depends(get_session)):
    payment = session.query(Payment).filter(payment.id == id).first() 
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id does not exist')
    session.delete(payment)
    return payment



import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
