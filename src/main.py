from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import src.db as db 

app = FastAPI(title="Project Tracker API")

# Data validation
class Project(BaseModel):
    id: int
    project_name: str
    status: str

class ProjectCreate(BaseModel):
    project_name: str

class Task(BaseModel):
    id: int
    project_id: int
    task_description: str

# API Endpoints 

@app.on_event("startup")
def on_startup():
    db.initialize_database()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Project Tracker API!"}

@app.post("/projects/", response_model=Project, status_code=201)
def create_project(project: ProjectCreate):
    """New project"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO projects (project_name) VALUES (%s)"
    cursor.execute(query, (project.project_name,))
    new_project_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": new_project_id, "project_name": project.project_name, "status": "Not Started"}

@app.get("/projects/{project_id}/tasks", response_model=List[Task])
def get_tasks_for_project(project_id: int):
    """Get all tasks"""
    conn = db.get_db_connection()
    cursor = conn.cursor(dictionary=True) # Return rows as dictionaries
    query = "SELECT id, project_id, task_description FROM tasks WHERE project_id = %s"
    cursor.execute(query, (project_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this project")
    return tasks