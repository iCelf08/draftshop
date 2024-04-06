from datetime import timedelta
from typing import List
import uuid
import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import authentication, security
from authentication import get_current_user
import models
import schemas
import crud
from db import get_db , engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# User endpoints

@app.post("/register", response_model=schemas.UserBase)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        **user.dict(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authentication.get_user(db, username=form_data.username)
    if not user or not security.pwd_context.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not valid credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me", response_model=schemas.UserBase)
async def read_users_me(current_user: schemas.UserBase = Depends(get_current_user)):
    return current_user

    
@app.put("/users/{username}", response_model=schemas.UserBase)
async def update_user(
    username: str,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(authentication.get_current_user)
):
    # Check if the current user is authorized to update the specified user
    if current_user.username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

    # Retrieve the user to be updated
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Perform the update operation
    updated_user = crud.update_user(db, username, user_update)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user")

    return updated_user
        
"""@app.get("/users/{email}", response_model=schemas.UserBase)
async def get_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user"""

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(authentication.get_current_user)
):
    # Check if the user trying to delete the account is the same as the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")
    
    deleted_user = crud.delete_user_by_id(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}



# Product endpoints

@app.get("/products/{id}", response_model=schemas.ProductBase)
async def get_product(id: uuid.UUID, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, id=id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/", response_model=List[schemas.ProductBase])
async def get_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@app.post("/products/", response_model=schemas.ProductBase)
async def add_product(product: schemas.ProductAdd, db: Session = Depends(get_db)):
    return crud.add_product(db=db, product=product)

@app.delete("/products/{id}")
async def delete_product(id: uuid.UUID, db: Session = Depends(get_db)):
    deleted_product = crud.delete_product(db, id=id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Order endpoints
@app.post("/orders/", response_model=schemas.OrderBase)
async def set_order(
    order_set: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(authentication.get_current_user)
):
    # Assuming `order_set` includes the user ID of the current user
    order_set.user_id = current_user.id
    
    return crud.set_order(db=db, order_data=order_set)

@app.put("/orders/{order_id}", response_model=schemas.OrderBase)
def update_order(
    order_id: uuid.UUID,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(authentication.get_current_user)
):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    # Check if the current user is authorized to update the order
    if db_order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this order")
    
    updated_order = crud.update_order(db, order_id, order_update)
    if updated_order is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update order")
    
    return updated_order

@app.delete("/orders/{id}")
async def delete_order(order_id: uuid.UUID, db: Session = Depends(get_db),current_user: schemas.UserBase = Depends(authentication.get_current_user)):
    deleted_order = crud.delete_order(db=db, order_id=order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

#Review Endpoints

@app.post("/reviews/", response_model=schemas.Review)
async def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(authentication.get_current_user)
):
    # Check if the product exists
    product = crud.get_product(db, id=review.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    created_review = crud.create_review(db=db, review=review, user_id=current_user.id)
    return created_review

@app.get("/reviews/{review_id}", response_model=schemas.Review)
def read_review(review_id: uuid.UUID, db: Session = Depends(get_db)):
    db_review = crud.get_review(db=db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review



@app.put("/reviews/{review_id}", response_model=schemas.Review)
def update_review(review_id: uuid.UUID, review: schemas.ReviewUpdate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(authentication.get_current_user)):
     
    db_review = crud.get_review(db=db, review_id=review_id)
    
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if db_review.review_maker_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this review")
    
    updated_review = crud.update_review(db=db, review_id=review_id, review=review)
    return updated_review



@app.delete("/reviews/{review_id}", response_model=schemas.Review)
def delete_review(review_id: uuid.UUID, db: Session = Depends(get_db), current_user: models.User = Depends(authentication.get_current_user)):
    db_review = crud.get_review(db=db, review_id=review_id)
    
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if db_review.review_maker_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this review")
    
    deleted_review = crud.delete_review(db=db, review_id=review_id)
    return deleted_review
