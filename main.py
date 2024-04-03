from typing import List
import uuid
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for getting database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User endpoints

@app.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
async def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.login(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Wrong email/password")
    return {"message": "User found"}

@app.get("/users/{email}", response_model=schemas.User)
async def get_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{email}")
async def delete_user(email: str, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, email)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Product endpoints

@app.get("/products/{id}", response_model=schemas.Product)
async def get_product(id: uuid.UUID, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, id=id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/", response_model=List[schemas.Product])
async def get_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@app.post("/products/", response_model=schemas.Product)
async def add_product(product: schemas.ProductAdd, db: Session = Depends(get_db)):
    return crud.add_product(db=db, product=product)

@app.delete("/products/{id}")
async def delete_product(id: uuid.UUID, db: Session = Depends(get_db)):
    deleted_product = crud.delete_product(db, id=id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Order endpoints

@app.post("/orders/", response_model=schemas.Order)
async def set_order(order_set: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.set_order(db=db, order=order_set)


@app.delete("/orders/{id}")
async def delete_order(order_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted_order = crud.delete_order(db=db, order_id=order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
