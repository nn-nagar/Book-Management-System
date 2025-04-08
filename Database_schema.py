# Database Schema

"""CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(50),
    year_published INTEGER,
    summary TEXT
);


CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    user_id INTEGER,
    review_text TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5)
);"""