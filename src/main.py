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


class TaskCreate(BaseModel):
    project_id: int
    task_description: str

class TaskUpdate(BaseModel):
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

@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    """New task"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO tasks (project_id, task_description) VALUES (%s, %s)"
    cursor.execute(query, (task.project_id, task.task_description))
    new_task_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": new_task_id, "project_id": task.project_id, "task_description": task.task_description}

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    """Update task"""
    conn = db.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Check if task exists
    query_check = "SELECT project_id FROM tasks WHERE id = %s"
    cursor.execute(query_check, (task_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    project_id = result['project_id']

    # Update the task
    query_update = "UPDATE tasks SET task_description = %s WHERE id = %s"
    cursor.execute(query_update, (task.task_description, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": task_id, "project_id": project_id, "task_description": task.task_description}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete task"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    # Check if task exists
    query_check = "SELECT id FROM tasks WHERE id = %s"
    cursor.execute(query_check, (task_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete the task
    query_delete = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(query_delete, (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return
