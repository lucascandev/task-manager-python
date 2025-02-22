import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry
from database import create_db, add_task, list_tasks, mark_as_completed, delete_task, edit_task
from notifications import check_due_tasks_gui
import threading
from datetime import datetime

# Criar banco de dados e tabela, caso não existam
create_db()

# Variável global para armazenar as tarefas
tasks = []

# Função para adicionar tarefa via interface gráfica
def add_task_gui():
    description = simpledialog.askstring("Nova Tarefa", "Descrição da tarefa:")
    
    if not description:
        messagebox.showwarning("Entrada inválida", "A descrição da tarefa não pode ser vazia.")
        return

    # Permitindo qualquer data escolhida no calendário (não permite digitação)
    due_date = cal_due_date.get_date()
    due_date_str = due_date.strftime("%d/%m/%Y")
    
    priority = priority_combobox.get()

    if priority and due_date_str:
        add_task(description, due_date_str, priority)
        load_tasks()
    else:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")

# Função para listar tarefas na interface gráfica
def load_tasks(page=1, per_page=10):
    global tasks
    tasks_listbox.delete(0, tk.END)
    tasks = list_tasks((page - 1) * per_page, per_page)

    for task in tasks:
        due_date = datetime.strptime(task[2], "%d/%m/%Y").strftime("%d/%m/%Y")
        task_str = f"{task[1]:<30} {due_date:<12} {task[3]:<10} {task[4]}"
        tasks_listbox.insert(tk.END, task_str)

# Função para marcar tarefa como concluída
def mark_completed():
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

# Função para excluir tarefa
def delete_task_gui():
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

# Função para editar tarefa
def edit_task_gui():
    selected_task = tasks_listbox.curselection()
    if selected_task:
        task_id = tasks[selected_task[0]][0]
        new_description = simpledialog.askstring("Editar Tarefa", "Nova descrição:")
        new_due_date = cal_due_date.get_date().strftime("%d/%m/%Y")
        new_priority = priority_combobox.get()

        if new_description and new_due_date and new_priority:
            edit_task(task_id, new_description, new_due_date, new_priority)
            load_tasks()
        else:
            messagebox.showwarning("Entrada inválida", "Todos os campos devem ser preenchidos.")
    else:
        messagebox.showwarning("Seleção inválida", "Selecione uma tarefa para editar.")

# Criar janela principal
root = tk.Tk()
root.title("Gestor de Tarefas")
root.geometry("500x500")

# Configurar o tema padrão
root.tk_setPalette(background="#f0f0f0")

# Configurar layout responsivo
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(0, weight=1)

# Seleção de prioridade
priority_label = ttk.Label(root, text="Selecione a Prioridade:")
priority_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

priority_combobox = ttk.Combobox(root, values=["Alta", "Média", "Baixa"], state="readonly")
priority_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Seletor de data de vencimento
date_label = ttk.Label(root, text="Data de Vencimento:")
date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Calendário onde o usuário só pode escolher a data (sem digitar)
cal_due_date = DateEntry(root, date_pattern="dd/mm/yyyy", width=12, state="readonly")  # 'state=readonly' impede digitação
cal_due_date.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Botões de ação
add_button = ttk.Button(root, text="Adicionar Tarefa", command=add_task_gui)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

mark_button = ttk.Button(root, text="Marcar como Concluída", command=mark_completed)
mark_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

delete_button = ttk.Button(root, text="Excluir Tarefa", command=delete_task_gui)
delete_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

edit_button = ttk.Button(root, text="Editar Tarefa", command=edit_task_gui)
edit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Lista de tarefas
tasks_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
tasks_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

# Carregar tarefas na interface
load_tasks()

# Iniciar o thread para notificações
notification_thread = threading.Thread(target=check_due_tasks_gui, daemon=True)
notification_thread.start()

# Iniciar a interface gráfica
root.mainloop()
