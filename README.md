# S3 Bucket Status Checker

## Overview
This application checks the status of S3 buckets by generating potential bucket names and verifying their HTTP status codes. It is structured in a modular way with separate components for web routing, bucket name generation, configuration, and database interactions.

## Components

### `app.py`
- **Description**: Handles web routing and server responses. It integrates all other components and provides HTTP endpoints to check bucket statuses and retrieve data from the database.
- **Endpoints**:
  - `/check/buckets/v1`: Generates bucket names, checks their statuses, and optionally stores results in a MongoDB database.
  - `/check/buckets/db/v1`: Retrieves bucket check results from the database.
  - `/`: Serves the home page.
  - `/help`: Provides help information about the application.

### `bucket_manager.py`
- **Description**: Responsible for generating S3 bucket names and checking their HTTP status.
- **Functions**:
  - `generate_bucket_names()`: Generates names based on specified criteria (currently all 5-letter lowercase combinations).
  - `check_s3_bucket_status(bucket_name, timeout)`: Checks the HTTP status of the given S3 bucket name.

### `config.py`
- **Description**: It can contains configuration settings for the application.

### `database.py`
- **Description**: Manages database operations including connecting to MongoDB and inserting results into the database.

### `docker-compose.yml`
- **Description**: Defines services, networks, and volumes for the application and MongoDB database, facilitating deployment via Docker.

## Setup and Running

### Requirements
- Docker
- Docker Compose

### Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
    ```

## Build and Run with Docker Compose:
1. **Run docker compose command**:
   ```bash
   docker-compose up --build
    ```

## Access the Application

- **Web Interface:** Visit [http://localhost:5000/](http://localhost:5000/) for the web interface.
- **Bucket Status Check:** Access [http://localhost:5000/check/buckets/v1](http://localhost:5000/check/buckets/v1) to start a bucket status check.
- **Database Results:** Access [http://localhost:5000/check/buckets/db/v1](http://localhost:5000/check/buckets/db/v1) to view results from the database.

## View Logs and Manage Services

Use Docker and Docker Compose commands to view logs, stop, and start services.

## Notes

- Modify `config.py` to adjust settings as needed before building if not using environment variables.
- Ensure MongoDB settings in `docker-compose.yml` are appropriate for your setup.

## Additional Information

### Modifying Bucket Name Generation

To change the criteria for bucket name generation, modify the `generate_bucket_names` function in `bucket_manager.py`.

### Database Schema

Document structure in MongoDB includes `name`, `status_code`, and MongoDB's `_id`.
