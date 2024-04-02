from typing import List, Generator
import uuid
import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Body, Query

import models
import format
import functions
from db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#UserENDPOINT---

@app.post("/register", response_model=format.UserInfo)
def create_user(user: format.UserCreate, db: Session = Depends(get_db)):
    db_user = functions.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return functions.create_user(db=db, user=user)


@app.post("/login")
async def login_user(user: format.UserLogin, db: Session = Depends(get_db)):
    db_user = functions.get_Login(db, email=user.email, password=user.password)
    if db_user == False:
        raise HTTPException(status_code=400, detail="Wrong email/password")
    return {"message": "User found"}


@app.get("/get_user/{email}", response_model=format.UserInfo)
async def get_user(email: str, db: Session = Depends(get_db)):
    db_user = functions.get_user_by_email(db, email=email)
    return db_user

@app.delete("/users/{email}")
async def delete_user(email: str, db: Session = Depends(get_db)):
    db_user = functions.delete_user(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.delete("/users/{email}")
async def delete_user(email: str, db: Session = Depends(get_db)):
    db_user = functions.delete_user(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

#ProductENDPOINTS --

@app.get("/products/{id}", response_model=format.ProductInfobase)
async def get_product(id:uuid.UUID, db: Session= Depends(get_db)):
    db_product = functions.get_product(db,id=id)
    if db_product is None:
          raise HTTPException(status_code=400, detail="No Product found")
    return db_product

@app.get("/products/", response_model=List[format.ProductInfobase])
async def get_products(db: Session = Depends(get_db)):
    products = functions.get_products(db)
    if products is None :
        raise HTTPException(status_code=400 , details="No products found") 
    return [
        {"name": product.name, "price": product.price, "brand": product.brand}
        for product in products
    ]


@app.post("/products/", response_model=format.ProductInfobase)
async def add_product(name: str, price: float, brand:str, db: Session = Depends(get_db)):
    product = format.ProductInfobase(name=name, price=price, brand=brand)
    db_product = functions.add_product(db, product)
    return db_product

@app.delete("/products/{id}")
async def delete_product(id: uuid.UUID, db: Session = Depends(get_db)):
    del_product = functions.delete_product(db, id=id)
    if del_product:
         raise HTTPException(status_code=200, detail="Product deleted Successfully")
    else:
        raise HTTPException(status_code=400, detail="Product Not found to delete")
    



#OrderENDPOINTS

@app.post("/orders/", response_model=format.OrderInfo)
async def set_order(order_set: format.OrderSet, db: Session = Depends(get_db)):
    return functions.set_order(db=db, user_id=order_set.user_id, product_ids=order_set.product_ids)


@app.delete("/orders/{id}")
async def delete_order(order_id:uuid.UUID, db:Session= Depends(get_db)):
    del_order = functions.delete_order(db=db, order_id = order_id)
    if del_order is not None:
        return {"message": "order deleted successfully"}
    raise HTTPException(status_code=404,detail="Order not found")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)