import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from database import create_db, add_task, list_tasks, mark_as_completed, delete_task, backup_to_json
from notifications import check_due_tasks_gui
import threading
from datetime import datetime

# Criar banco de dados e tabela, caso não existam
create_db()

# Função para adicionar tarefa via interface gráfica
def add_task_gui():
    description = simpledialog.askstring("Nova Tarefa", "Descrição da tarefa:")
    
    if description:
        # Seletor de data
        due_date = cal_due_date.get_date()
        # Verificar se a data é válida (não passada)
        if due_date < datetime.now().date():
            messagebox.showwarning("Data inválida", "A data de vencimento não pode ser no passado.")
            return
        
        # Formatar data para o formato DD/MM/YYYY (usado no banco de dados)
        due_date_str = due_date.strftime("%d/%m/%Y")
        
        # Seleção de prioridade
        priority = priority_combobox.get()

        if priority and due_date_str:
            add_task(description, due_date_str, priority)
            load_tasks()
        else:
            messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")
    else:
        messagebox.showwarning("Entrada inválida", "Por favor, adicione uma descrição para a tarefa.")

# Função para listar tarefas na interface gráfica
def load_tasks(order_by="due_date"):
    global tasks  # Referência à variável global
    tasks_listbox.delete(0, tk.END)
    tasks = list_tasks(order_by)  # Carrega as tarefas do banco de dados

    for task in tasks:
        due_date = datetime.strptime(task[2], "%d/%m/%Y").strftime("%d/%m/%Y")
        task_str = f"{task[1]} - {due_date} - {task[3]} - {task[4]}"
        tasks_listbox.insert(tk.END, task_str)

# Função para marcar tarefa como concluída
def mark_completed():
    try:
        selected_task = tasks_listbox.curselection()
        if selected_task:
            task_id = tasks[selected_task[0]][0]  # Usa a variável global 'tasks'
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
            task_id = tasks[selected_task[0]][0]  # Usa a variável global 'tasks'
            delete_task(task_id)
            load_tasks()
        else:
            messagebox.showwarning("Seleção inválida", "Selecione uma tarefa para excluir.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para backup de tarefas
def backup_gui():
    try:
        backup_to_json()
        messagebox.showinfo("Backup", "Backup das tarefas realizado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao realizar backup: {e}")

# Função de ordenação
def sort_by_priority():
    load_tasks(order_by="priority")

def sort_by_date():
    load_tasks(order_by="due_date")

# Criar janela principal
root = tk.Tk()
root.title("Gestor de Tarefas")
root.geometry("500x500")  # Tamanho inicial da janela

# Seletor de prioridade
priority_label = ttk.Label(root, text="Selecione a Prioridade:")
priority_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

priority_combobox = ttk.Combobox(root, values=["Alta", "Média", "Baixa"], state="readonly")
priority_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Seletor de data de vencimento
date_label = ttk.Label(root, text="Data de Vencimento:")
date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

cal_due_date = DateEntry(root, date_pattern="dd/mm/yyyy", width=12, state="normal")
cal_due_date.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Botões de ação
add_button = ttk.Button(root, text="Adicionar Tarefa", command=add_task_gui)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

mark_button = ttk.Button(root, text="Marcar como Concluída", command=mark_completed)
mark_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

delete_button = ttk.Button(root, text="Excluir Tarefa", command=delete_task_gui)
delete_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Botão de backup
backup_button = ttk.Button(root, text="Fazer Backup", command=backup_gui)
backup_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Lista de tarefas
tasks_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
tasks_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

# Ordenação de tarefas
sort_priority_button = ttk.Button(root, text="Ordenar por Prioridade", command=sort_by_priority)
sort_priority_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

sort_date_button = ttk.Button(root, text="Ordenar por Data", command=sort_by_date)
sort_date_button.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

# Carregar tarefas na interface
load_tasks()

# Iniciar o thread para notificações
notification_thread = threading.Thread(target=check_due_tasks_gui, daemon=True)
notification_thread.start()

# Iniciar a interface gráfica
root.mainloop()
