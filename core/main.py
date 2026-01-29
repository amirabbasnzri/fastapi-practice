from fastapi import FastAPI, status, HTTPException, Query, Depends
from fastapi_swagger import patch_fastapi
from database import engine, Base, get_session
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List
from sqlalchemy.orm import Session
from schemas import (
    PaymentCreateSchema,
    PaymentReadSchema,
    PaymentUpdateSchema,
    PaymentDeleteSchema,
    PaymentResponseSchema,
)
from models import Payment

# application: ---------------------------------------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is started")
    Base.metadata.create_all(engine)
    yield
    print("Application is shutdown")


app = FastAPI(lifespan=lifespan, docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/swagger")


payments_db = [
    {"id": 1, "description": "to buy a laptop", "amount($)": 2100.2},
    {"id": 2, "description": "to buy a phone", "amount($)": 1100.9},
    {"id": 3, "description": "to buy a speaker", "amount($)": 900.8},
    {"id": 4, "description": "to buy a course", "amount($)": 200.0},
    {"id": 5, "description": "to buy a television", "amount($)": 3400.0},
    {"id": 6, "description": "to buy earbuds", "amount($)": 600.5},
    {"id": 7, "description": "to buy a smart watch", "amount($)": 800},
]

@app.post("/payments/add", status_code=status.HTTP_201_CREATED, response_model=PaymentResponseSchema,)
def add_payment(request: PaymentCreateSchema, session: Session = Depends(get_session)):
    new_payment = Payment(id=1, description=request.description , amount=request.amount)
    session.add(new_payment)

@app.get("/payments", response_model=List[PaymentResponseSchema])
def see_payments():
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"Payments list": list(payments_db)},
    )


@app.get("/payments/id/{id}", response_model=PaymentResponseSchema)
def see_item_by_id(item_id: int = Query(alias="object_id")):
    for obj in payments_db:
        if obj["id"] == item_id:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, content={"message": obj}
            )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Id does not exist"
    )


@app.put("/payments/edit/{id}", response_model=PaymentResponseSchema)
def update_amount_by_id(PUS: PaymentUpdateSchema):
    for obj in payments_db:
        if obj["id"] == PUS.id:
            obj["amount"] = PUS.amount
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": f"Item with ID {obj['id']} updated successfully"},
            )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Id does not exist"
    )


@app.delete("/payments/delete/{id}", response_model=PaymentResponseSchema)
def delete_item_by_id(PDS: PaymentDeleteSchema):
    for obj in payments_db:
        if obj["id"] == PDS.id:
            payments_db.remove(obj)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": f"Item with ID {PDS.id} removed successfully"},
            )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Id does not exist"
    )


import uvicorn


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
