# Intelligent Book Management System

## Overview
The **Intelligent Book Management System** is a Python-based application that utilizes a locally running **Llama3 generative AI model** and **cloud infrastructure** to manage books efficiently. The system enables users to **add, retrieve, update, and delete books** from a **PostgreSQL database**, generate **summaries for books**, and provide **book recommendations** based on user preferences. Additionally, it manages **user reviews** and generates **ratings and review summaries** for books.

## Features
- **Book Management**: CRUD (Create, Read, Update, Delete) operations for books in a PostgreSQL database.
- **AI-Generated Summaries**: Uses Llama3 to generate summaries for books.
- **Book Recommendations**: Suggests books based on user preferences.
- **User Reviews & Ratings**: Allows users to submit reviews and ratings for books.
- **Review Summarization**: Generates summaries of book reviews.
- **RESTful API**: Exposes functionality via an API for easy integration.
- **Cloud Deployment**: The system is deployable on cloud platforms like AWS.

## Technologies Used
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL
- **AI Model**: Llama3 (Running Locally)
- **Cloud Services**: AWS (EC2, RDS, S3, Lambda, API Gateway)
- **Authentication**: JWT-based authentication

## Installation & Setup
### Prerequisites
- Python 3.9+
- PostgreSQL
- Docker (optional for containerized deployment)
- Llama3 AI Model setup

### Step 1: Clone the Repository
```sh
git clone https://github.com/nn-nagar/Book-Management-System.git
cd Book-Management-System
```

### Step 2: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 3: Setup Database
Ensure PostgreSQL is running and create a database:
```sh
CREATE DATABASE book_management;
```
Update the `.env` file with your database credentials.

### Step 4: Start the Application
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 5: Access the API
Open [http://localhost:8000/docs](http://localhost:8000/docs) to explore API endpoints.

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | /books | Get all books |
| POST | /books | Add a new book |
| GET | /books/{id} | Retrieve a specific book |
| PUT | /books/{id} | Update book details |
| DELETE | /books/{id} | Delete a book |
| POST | /books/{id}/summarize | Generate book summary using Llama3 |
| GET | /books/{id}/recommendations | Get book recommendations |
| POST | /books/{id}/reviews | Add a user review |
| GET | /books/{id}/reviews/summary | Get summarized book reviews |


## 🔐 **User Authentication & Token Management – Code Overview**

### 📌 **Purpose:**
This code implements **secure user authentication** using **OAuth2 with JWT (JSON Web Tokens)**. It allows users to log in with credentials, receive a token, and access protected routes based on their identity.

---

### 📍 **Authentication Flow - Explained in Steps**

1. ### **`authenticate_user()`**
   - **Purpose:** Validates if the provided username and password match a user in the database.
   - **Logic:**
     - Fetches the user by username using `get_user()`.
     - Verifies the provided password against the stored hashed password using `verify_password()`.
     - Returns the user object if valid, otherwise returns `False`.

2. ### **`create_access_token()`**
   - **Purpose:** Generates a JWT access token that encodes user data with an expiration.
   - **Logic:**
     - Takes user data (usually the username).
     - Adds an expiration timestamp (default: 15 minutes if not provided).
     - Encodes the token using a secret key and specified algorithm.

3. ### **`get_current_user()`**
   - **Purpose:** A dependency function used to protect routes and fetch the current authenticated user from the token.
   - **Logic:**
     - Decodes the token using the secret key.
     - Extracts the username from the token payload.
     - Validates the existence of the user.
     - Raises an exception if the token is invalid or the user doesn’t exist.

---

### 🧪 **Token-Based Authentication Endpoint**

4. ### **`@app.post("/token")`**
   - **Purpose:** Login endpoint that validates user credentials and issues a JWT token.
   - **Logic:**
     - Accepts login form data (username and password).
     - Calls `authenticate_user()` to verify credentials.
     - If valid, generates an access token with `create_access_token()`.
     - Returns the token to the client with `"token_type": "bearer"`.

---

### 🔒 **Protected Endpoint**

5. ### **`@app.get("/users/me")`**
   - **Purpose:** A protected route that returns the authenticated user's profile data.
   - **Logic:**
     - Uses `Depends(get_current_user)` to extract and verify the user from the token.
     - Returns the authenticated user object.

---

### ✅ **Summary - What This Code Does**
- Implements **user login and session handling** using JWT.
- Ensures **password security** via hashing (not shown but implied with `verify_password`).
- Protects routes using FastAPI's dependency injection (`Depends()`).
- Issues **short-lived tokens** to reduce security risk.
- Uses **OAuth2 password grant flow**, commonly used in APIs.

---

## Deployment
### Docker
To run the system in a Docker container:
```sh
docker build -t book-management .
docker run -p 8000:8000 book-management
```

### Cloud Deployment (AWS)
1. Deploy the PostgreSQL database on AWS RDS.
2. Run the application on AWS EC2 or a containerized environment (EKS/Fargate).
3. Use AWS Lambda and API Gateway for serverless API management.

## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your fork and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any queries, reach out via [GitHub Issues](git clone https://github.com/nn-nagar/Book-Management-System.git).

