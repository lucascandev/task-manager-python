import sqlite3
from datetime import datetime

# Função para criar o banco de dados e a tabela de tarefas
def create_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

# Função para adicionar uma nova tarefa
def add_task(description, due_date, priority):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO tasks (description, due_date, priority, status)
    VALUES (?, ?, ?, ?)
    """, (description, due_date, priority, "pendente"))
    
    conn.commit()
    conn.close()

# Função para listar todas as tarefas
def list_tasks(order_by="due_date"):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    query = f"SELECT id, description, due_date, priority, status FROM tasks ORDER BY {order_by} ASC"
    cursor.execute(query)
    tasks = cursor.fetchall()
    
    conn.close()
    return tasks

# Função para marcar uma tarefa como concluída
def mark_as_completed(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE tasks
    SET status = 'concluída'
    WHERE id = ?
    """, (task_id,))
    
    conn.commit()
    conn.close()

# Função para excluir uma tarefa
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    conn.commit()
    conn.close()