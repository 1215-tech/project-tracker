# Personal Project Tracker API
## Still WIP some features may not work correctly

A simple API to track projects and their tasks, built with Python, FastAPI, MySQL, and Docker. This project was created to demonstrate skills in backend development, database management, and containerization.

## Tech Stack
- **Backend:** Python, FastAPI
- **Database:** MySQL
- **Containerization:** Docker, Docker Compose

## How to Run
1.  **Prerequisites:** You must have Docker and Docker Compose installed.
2.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/project-tracker.git](https://github.com/your-username/project-tracker.git)
    cd project-tracker
    ```
3.  **Run the application:**
    ```sh
    docker-compose up --build
    ```
4.  **Access the API:**
    - The API will be running at `http://127.0.0.1:8000`
    - Interactive documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`

## API Endpoints
- `POST /projects/`: Create a new project.
- `GET /projects/{project_id}/tasks`: Get all tasks for a specific project.