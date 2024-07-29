# Theater Ticket Booking System

This project is a theater ticket booking system with FastAPI, SQLAlchemy, and Redis. It provides functionality for checking available seats, booking seats, and temporarily reserving seats with an expiry time.

## Features

- Check available theaters.
- Check available seats in a theater.
- Book a seat (idempotent operation).
- Temporarily reserve a seat with an expiry time.
- Caching for seat availability. We will cache only those object which are not booked.

## Requirements

- Docker
- Docker Compose

### Setting Up the Project

1. **Clone the Repository**:
    ```sh
    git clone git@github.com:pranaybankar/ticketing_system.git
    ```
    ```sh
    cd theater_booking
    ```

2. **Build and Run the Docker Containers**:
    ```sh
    docker-compose up --build
    ```

3. **Access the Application**:
    - The FastAPI application will be available at [http://localhost:8000](http://localhost:8000).

4. **API Endpoints**:
    - `GET /theaters`: Retrieves all theater information.
    - `GET /theaters/{theaterId}/seats`: Retrieves the current availability of seats for a specified theater.
    - `POST /theaters/{theaterId}/book`: Books a seat for a specified theater.
    - `POST /theaters/{theaterId}/reserve`: Temporarily reserves a seat for a specified theater with an expiry time of five minutes.

5. **How to use the API Endpoints**:
    - `GET /theaters`: Run this first to retrieves all theatre information. Using this you get to know the Theatre `id` and `name`.
    - `GET /theaters/{theaterId}/seats`: Using the information from the earlier API you can check how many seats are available in the particular theatre. So, you can retrieve the current availability of seats for a specified theatre. So, you will get the `id`, `seat_number`, `is_booked` and `theater_id`.
   - `POST /theaters/{theaterId}/reserve`: To temporarily reserves a seat for a specified theatre provide the Theatre id and the seat number from the earlier API. The seat will be reserved for 5 mins to book. If you make a mistake in providing the seat number the API will return the available seat numbers.
    - `POST /theaters/{theaterId}/book`: Now to book your ticket specify the Theatre Id and the seart number to books a seat for the specified theatre. If you make a mistake in providing the seat number the API will return the available seat numbers.

6. **Stopping the Containers**:
    ```sh
    docker-compose down
    ```

### Notes
- Ensure Docker and Docker Compose are installed on your machine.
- The application uses Sqlite as the database and Redis for caching.
- I have used Swagger UI to interact with the APIs.
- You can update the RESERVATION_TIMEOUT in `docker-compose.yml` file.

This setup ensures your theater ticket booking system is containerized, easy to deploy, and scalable.

