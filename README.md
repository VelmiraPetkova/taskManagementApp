# Task Management Application

## Overview

The Task Management Application is a web-based tool designed to help users efficiently manage their tasks. It offers user authentication and authorization features, and allows creating, editing, and deleting tasks. You can also assign a task to a specific user by providing their user ID.

## Features

* User registration and login with authentication
* Create, edit, view, and delete tasks
* Responsive and user-friendly frontend interface

## Architecture

The application follows a client-server architecture:

* **Frontend:** JavaScript-based interface that handles user interactions and UI rendering
* **Backend:** Python with the Flask framework, managing API endpoints, authentication, authorization, and business logic
* **Database:** MySQL, used to store user and task data
* **Authentication & Authorization:** Implemented using Flask extensions or JWTs to secure endpoints and enforce role-based access control
* **Environment Management:** Environment variables and config files allow smooth switching between different database setups

## Technologies

* **Frontend:** JavaScript
* **Backend:** Python, Flask
* **Database:** MySQL
* **Authentication:** JWT (JSON Web Tokens)
* **Other tools:** SQLAlchemy or MySQL Connector for database interactions

## Installation

### Running with Docker Compose (Recommended)
This project includes a docker-compose.yml file to easily run the entire app stack (database, backend, frontend) with Docker:

1. **Clone the repository:**

```bash

git clone https://github.com/VelmiraPetkova/taskManagementApp.git
```
2. **Navigate to the project directory:**

```bash

cd taskManagementApp
```
3. **Run the docker compose:**

```bash

docker-compose up --build
```

Open your browser at http://localhost:3000 — you should see the frontend.

The frontend communicates with the backend at http://localhost:5001

The backend uses the database container db:3306 (inside Docker's internal network)

4. **To stop the containers::**

```bash

docker-compose down

```

## Screenshots
<!-- Add screenshots here -->
<img width="734" alt="image" src="https://github.com/user-attachments/assets/617dae3e-8cc7-43ad-9106-52216e08ffbd" />
<img width="734" alt="image" src="https://github.com/user-attachments/assets/f46b6f99-23c8-4fdb-ad58-c9fa9e71c862"/>




