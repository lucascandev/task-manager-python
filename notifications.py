import time
from datetime import datetime
from database import list_tasks
from tkinter import messagebox

# Função para verificar tarefas vencidas
def check_due_tasks_gui():
    try:
        tasks = list_tasks()  # Obter todas as tarefas
        current_date = datetime.now().strftime("%d/%m/%Y")

        for task in tasks:
            task_due_date_obj = datetime.strptime(task[2], "%d/%m/%Y")
            current_date_obj = datetime.strptime(current_date, "%d/%m/%Y")

            if task_due_date_obj < current_date_obj and task[4] != 'concluída':
                messagebox.showinfo("Tarefa Vencida", f"A tarefa '{task[1]}' está vencida desde {task[2]}.")
    except Exception as e:
        print(f"Erro ao verificar tarefas vencidas: {e}")

    time.sleep(60)  # A cada 60 segundos, verifica novamente
    check_due_tasks_gui()
