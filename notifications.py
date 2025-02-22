import time
from datetime import datetime
from database import list_tasks
from tkinter import messagebox

def check_due_tasks_gui(root):
    """Verifica se há tarefas vencidas e exibe uma notificação."""
    try:
        tasks = list_tasks()  # Obter todas as tarefas

        current_date = datetime.now().strftime("%Y-%m-%d")  # Data atual

        for task in tasks:
            task_due_date = task[2]  # A data de vencimento da tarefa
            task_due_date_obj = datetime.strptime(task_due_date, "%Y-%m-%d")
            current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")

            if task_due_date_obj < current_date_obj and task[4] != 'concluída':
                messagebox.showinfo("Tarefa Vencida", f"A tarefa '{task[1]}' está vencida desde {task_due_date}.")
    except Exception as e:
        print(f"Erro ao verificar tarefas vencidas: {e}")

    # Agendar a próxima execução após 60 segundos
    root.after(60000, check_due_tasks_gui, root)
