# MyNotes - Async Web Application with FastAPI
This project is an asynchronous web application built with FastAPI that provides a personal notes management service. The application allows users to create, edit, delete, and search notes using tags. Additionally, a Telegram bot is implemented to interact with the API for note management. All services are containerized with Docker.
## Technologies Used
- FastAPI - Fast and async web framework for building APIs.
- SQLAlchemy - ORM for managing database interactions.
- PostgreSQL - Relational database for note storage.
- Aiogram - Asynchronous Telegram bot framework.
- Docker - Containerization of services.
- JWT - For secure user authentication and authorization.
- Alembic - Database migration tool for SQLAlchemy.

## Description

__MyNotes__ is a microservice-based application designed to facilitate personal note management. It consists of the following components:

- backend: A FastAPI service that handles user authentication, CRUD operations for notes, and integration with the PostgreSQL database.
- telegram_bot: A Telegram bot built using Aiogram, which interacts with the FastAPI backend to allow users to manage their notes directly from Telegram.
- PostgreSQL: A relational database for storing user data and notes.
- Docker: Used for containerizing the services, ensuring easy setup and deployment.

The application uses JWT tokens for secure authentication and implements rate limiting to protect against excessive API requests.

## Setup Instructions
### Prerequisites

Docker and Docker Compose must be installed on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/MyNotes.git
cd MyNotes
```
#### Setting Up the Environment
1. __Configure Environment Variables.__

    Create a .env file in both backend/ and telegram_bot/ directories and add the necessary environment variables. 
2. __Start Docker Compose__

    Use the following command to build and start all services (FastAPI backend, PostgreSQL, and Telegram bot) using Docker Compose:
```bash
make up
```
3. __Make apply__
    
## Makefile Commands
- Start Services
```bash
make up
```
- Stop Services
```bash
make down
```
- Build Docker Images
```bash
make build
```
- View Logs
```bash
make logs
```
- Create migrations
```bash
make make_migration
```
- Apply migrations
```bash
make migrate
```
