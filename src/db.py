import mysql.connector
import os
import time

def get_db_connection():
    """Establishes a connection db"""
    for i in range(10): 
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DATABASE_HOST", "localhost"),
                user=os.getenv("DATABASE_USER", "user"),
                password=os.getenv("DATABASE_PASSWORD", "password"),
                database=os.getenv("DATABASE_NAME", "project_db")
            )
            print("Database connection successful.")
            return conn
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}. Retrying in 5 seconds...")
            time.sleep(5)
    return None

def initialize_database():
    """Creates the necessary tables if needed"""
    conn = get_db_connection()
    if not conn:
        print("Could not establish database connection. Exiting.")
        return

    cursor = conn.cursor()

    # 'projects' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        project_name VARCHAR(255) NOT NULL,
        status VARCHAR(50) DEFAULT 'Not Started',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 'tasks' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        project_id INT NOT NULL,
        task_description TEXT NOT NULL,
        due_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    )
    """)

    print("Database initialized successfully.")
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()