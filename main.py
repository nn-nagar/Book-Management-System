from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import Optional, List
import asyncio
from Utilities import *


SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# OAuth2
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class Review(BaseModel):
    id: int
    book_id: int
    user_id: int
    review_text: str
    rating: int

# creation of  database
users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": "hased_password"  # password: "password"
    }
}

def authenticate_user(users_db, username: str, password: str):
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# instance
app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Book endpoints
@app.post("/books", response_model=Book)
async def create_book(book: Book, current_user: User = Depends(get_current_user)):
    # Add book to the database
    async with SessionLocal() as session:
        new_book = BookModel(**book.dict())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
    return new_book

@app.get("/books", response_model=List[Book])
async def read_books(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        result = await session.execute(select(BookModel).offset(skip).limit(limit))
        books = result.scalars().all()
    return books

@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalar_one_or_none()
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        await session.commit()
        await session.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_id: int, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalar_one_or_none()
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        await session.delete(db_book)
        await session.commit()
    return {"message": "Book deleted"}

# Review
@app.post("/books/{book_id}/reviews", response_model=Review)
async def create_review(book_id: int, review: Review, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        new_review = ReviewModel(book_id=book_id, **review.dict())
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
    return new_review

@app.get("/books/{book_id}/reviews", response_model=List[Review])
async def read_reviews(book_id: int, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        result = await session.execute(select(ReviewModel).where(ReviewModel.book_id == book_id))
        reviews = result.scalars().all()
    return reviews


@app.get("/books/{book_id}/summary", response_model=dict)
async def get_summary(book_id: int, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
    summary = generate_summary(book.content)
    return {"summary": summary}

@app.get("/recommendations", response_model=List[str])
async def get_recommendations(genre: str, min_rating: int, current_user: User = Depends(get_current_user)):
    recommendations = recommend_books(genre, min_rating)
    return recommendations

@app.post("/generate-summary", response_model=dict)
async def generate_summary_endpoint(content: str, current_user: User = Depends(get_current_user)):
    summary = generate_summary(content)
    return {"summary": summary}

# Models for ORM
from sqlalchemy import Column, Integer, String, Text, ForeignKey

class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String, index=True)
    year_published = Column(Integer, index=True)
    summary = Column(Text, index=True)

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), index=True)
    user_id = Column(Integer, index=True)
    review_text = Column(Text, index=True)
    rating = Column(Integer, index=True)

# database tables


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_db_and_tables())

