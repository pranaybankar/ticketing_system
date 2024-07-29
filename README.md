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
   - The data is already feeded in SQLITE DB, if you want to update the data please add it in `app/data/theaters.json` and `app/data/seats.json` before running the below commnads.
    ```sh
    docker-compose up --build
    ```

4. **Access the Application**:
    - The FastAPI application will be available at [http://localhost:8000](http://localhost:8000).

5. **API Endpoints**:
    - `GET /theaters`: Retrieves all theater information.
    - `GET /theaters/{theaterId}/seats`: Retrieves the current availability of seats for a specified theater.
    - `POST /theaters/{theaterId}/book`: Books a seat for a specified theater.
    - `POST /theaters/{theaterId}/reserve`: Temporarily reserves a seat for a specified theater with an expiry time of five minutes.

6. **How to use the API Endpoints**:
    - To try any API click on the `Try it out` button.<img width="874" alt="image" src="https://github.com/user-attachments/assets/536806da-ba08-4770-93cd-f38e04150daf">
    - `GET /theaters`: Run this first to retrieves all theatre information. Using this you get to know the Theatre `id` and `name`. <img width="860" alt="image" src="https://github.com/user-attachments/assets/a5aabd98-c051-4eef-8553-5b22a3a81a5f">
    - `GET /theaters/{theaterId}/seats`: Using the information from the earlier API you can check how many seats are available in the particular theatre. So, you can retrieve the current availability of seats for a specified theatre. So, you will get the `id`, `seat_number`, `is_booked` and `theater_id`. <img width="876" alt="image" src="https://github.com/user-attachments/assets/3f303990-e93b-4ca4-b806-6e4c622e50a1"> <img width="866" alt="image" src="https://github.com/user-attachments/assets/31a11662-e350-44db-a44f-38cf9ea15027">
   - `POST /theaters/{theaterId}/reserve`: To temporarily reserves a seat for a specified theatre provide the Theatre id and the seat number from the earlier API. The seat will be reserved for 5 mins to book. If you make a mistake in providing the seat number the API will return the available seat numbers. Note: You need to provide the `theatre_id` as a path parameter and `seat_number` as a body payload parameter.<img width="874" alt="image" src="https://github.com/user-attachments/assets/92c035d9-5dc0-47f4-90a8-a323a2dc114f"> <img width="874" alt="image" src="https://github.com/user-attachments/assets/86ce1882-2d22-46ab-8ae2-0e2fc8036f2d">
    - `POST /theaters/{theaterId}/book`: Now to book your ticket specify the Theatre Id and the seart number to books a seat for the specified theatre. If you make a mistake in providing the seat number the API will return the available seat numbers. Note: You need to provide the `theatre_id` as a path parameter and `seat_number` as a body payload parameter. <img width="891" alt="image" src="https://github.com/user-attachments/assets/59f04ed7-8caa-4d5c-8605-4e0851835c9c"> <img width="871" alt="image" src="https://github.com/user-attachments/assets/c54ba9d8-ee61-4086-b472-f2552134446e">

8. **Stopping the Containers**:
    ```sh
    docker-compose down
    ```

### Notes
- Ensure Docker and Docker Compose are installed on your machine.
- The application uses Sqlite as the database and Redis for caching.
- I have used Swagger UI to interact with the APIs.
- You can update the RESERVATION_TIMEOUT in `docker-compose.yml` file.

This setup ensures your theater ticket booking system is containerized, easy to deploy, and scalable.

