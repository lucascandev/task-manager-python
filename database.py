import sqlite3

def create_db():
    """Cria o banco de dados e a tabela de tarefas, se não existirem."""
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        # Criação da tabela se não existir
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            due_date DATE NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados ou tabela: {e}")
    finally:
        conn.close()

def add_task(description, due_date, priority):
    """Adiciona uma nova tarefa ao banco de dados."""
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tasks (description, due_date, priority, status)
        VALUES (?, ?, ?, ?)
        """, (description, due_date, priority, "pendente"))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar tarefa: {e}")
    finally:
        conn.close()

def list_tasks():
    """Retorna todas as tarefas do banco de dados."""
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, description, due_date, priority, status FROM tasks ORDER BY due_date ASC")
        tasks = cursor.fetchall()
        return tasks
    except sqlite3.Error as e:
        print(f"Erro ao listar tarefas: {e}")
        return []
    finally:
        conn.close()

def mark_as_completed(task_id):
    """Marca uma tarefa como concluída."""
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE tasks
        SET status = 'concluída'
        WHERE id = ?
        """, (task_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao marcar tarefa como concluída: {e}")
    finally:
        conn.close()

def delete_task(task_id):
    """Exclui uma tarefa do banco de dados."""
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir tarefa: {e}")
    finally:
        conn.close()
