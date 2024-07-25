# Theater Ticket Booking System

This project is a theater ticket booking system with FastAPI, SQLAlchemy, and Redis. It provides functionality for checking available seats, booking seats, and temporarily reserving seats with an expiry time.

## Features

- Check available seats
- Book a seat (idempotent operation)
- Temporarily reserve a seat with an expiry time
- Caching for seat availability

## Requirements

- Docker
- Docker Compose

### Setting Up the Project

1. **Clone the Repository**:
    ```sh
    git clone <repository-url>
    cd theater_booking
    ```

2. **Build and Run the Docker Containers**:
    ```sh
    docker-compose up --build
    ```

3. **Access the Application**:
    - The FastAPI application will be available at [http://localhost:8000](http://localhost:8000).

4. **API Endpoints**:
    - `GET /theaters/{theaterId}/seats`: Retrieves the current availability of seats for a specified theater.
    - `POST /theaters/{theaterId}/book`: Books a seat for a specified theater.
    - `POST /theaters/{theaterId}/reserve`: Temporarily reserves a seat for a specified theater with an expiry time.

5. **Stopping the Containers**:
    ```sh
    docker-compose down
    ```

### Notes
- Ensure Docker and Docker Compose are installed on your machine.
- The application uses PostgreSQL as the database and Redis for caching.

This setup ensures your theater ticket booking system is containerized, easy to deploy, and scalable.

