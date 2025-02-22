import time
from datetime import datetime
from database import list_tasks
from tkinter import messagebox

# Função para verificar tarefas vencidas
def check_due_tasks_gui():
    while True:
        try:
            tasks = list_tasks()  # Obter todas as tarefas

            current_date = datetime.now().strftime("%d/%m/%Y")

            for task in tasks:
                task_due_date = task[2]  # A data de vencimento da tarefa
                task_due_date_obj = datetime.strptime(task_due_date, "%d/%m/%Y")
                current_date_obj = datetime.strptime(current_date, "%d/%m/%Y")

                # Se a tarefa estiver vencida e não foi concluída
                if task_due_date_obj < current_date_obj and task[4] != 'concluída':
                    messagebox.showinfo("Tarefa Vencida", f"A tarefa '{task[1]}' está vencida desde {task_due_date}.")
        
        except Exception as e:
            print(f"Erro ao verificar tarefas vencidas: {e}")
        
        time.sleep(60)  # A cada 60 segundos, verifica novamente
