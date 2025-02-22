import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry
from database import create_db, add_task, list_tasks, mark_as_completed, delete_task
from notifications import check_due_tasks_gui
from datetime import datetime

# Criar banco de dados e tabela, caso não existam
create_db()

# Variável global para armazenar as tarefas
tasks = []

def add_task_gui():
    """Adiciona uma nova tarefa via interface gráfica."""
    description = simpledialog.askstring("Nova Tarefa", "Descrição da tarefa:")

    if description:
        due_date = cal_due_date.get_date()
        # Verificar se a data de vencimento não é no futuro
        if due_date < datetime.now().date():
            messagebox.showwarning("Data inválida", "A data de vencimento não pode ser no passado.")
            return

        due_date_str = due_date.strftime("%Y-%m-%d")  # Formato de data 'YYYY-MM-DD'
        priority = priority_combobox.get()

        if priority:
            add_task(description, due_date_str, priority)
            load_tasks()
        else:
            messagebox.showwarning("Entrada inválida", "Por favor, selecione a prioridade da tarefa.")
    else:
        messagebox.showwarning("Entrada inválida", "Por favor, adicione uma descrição para a tarefa.")

def load_tasks():
    """Carrega e exibe todas as tarefas na interface gráfica."""
    global tasks
    tasks_listbox.delete(0, tk.END)
    tasks = list_tasks()  # Carregar tarefas do banco de dados

    for task in tasks:
        due_date = datetime.strptime(task[2], "%Y-%m-%d").strftime("%d/%m/%Y")
        task_str = f"{task[1]} - {due_date} - {task[3]} - {task[4]}"
        tasks_listbox.insert(tk.END, task_str)

def mark_completed():
    """Marca a tarefa selecionada como concluída."""
    try:
        selected_task = tasks_listbox.curselection()
        if selected_task:
            task_id = tasks[selected_task[0]][0]
            mark_as_completed(task_id)
            load_tasks()
        else:
            messagebox.showwarning("Seleção inválida", "Selecione uma tarefa para marcar como concluída.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def delete_task_gui():
    """Exclui a tarefa selecionada."""
    try:
        selected_task = tasks_listbox.curselection()
        if selected_task:
            task_id = tasks[selected_task[0]][0]
            delete_task(task_id)
            load_tasks()
        else:
            messagebox.showwarning("Seleção inválida", "Selecione uma tarefa para excluir.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Criar a janela principal
root = tk.Tk()
root.title("Gestor de Tarefas")
root.geometry("500x500")  # Tamanho inicial da janela

# Configurar layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(0, weight=1)

# Labels e entradas
priority_label = ttk.Label(root, text="Selecione a Prioridade:")
priority_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

priority_combobox = ttk.Combobox(root, values=["Alta", "Média", "Baixa"], state="readonly")
priority_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

date_label = ttk.Label(root, text="Data de Vencimento:")
date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Seletor de data de vencimento (sem permitir que o usuário escreva)
cal_due_date = DateEntry(root, date_pattern="dd/mm/yyyy", width=12, state="readonly")
cal_due_date.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Botões de ação
add_button = ttk.Button(root, text="Adicionar Tarefa", command=add_task_gui)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

mark_button = ttk.Button(root, text="Marcar como Concluída", command=mark_completed)
mark_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

delete_button = ttk.Button(root, text="Excluir Tarefa", command=delete_task_gui)
delete_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Lista de tarefas
tasks_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
tasks_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

# Carregar tarefas na interface
load_tasks()

# Iniciar o processo de verificação de tarefas vencidas
root.after(60000, check_due_tasks_gui, root)  # Passando root para a função

# Iniciar a interface gráfica
root.mainloop()
