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

