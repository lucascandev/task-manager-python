import customtkinter as ctk
from tkinter import simpledialog, messagebox
from tkcalendar import DateEntry
from database import create_db, add_task, list_tasks, mark_as_completed, delete_task
import threading
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
import webbrowser  # Importando para abrir links no navegador

# Criar banco de dados e tabela, caso não existam
create_db()

# Variável global para manter o ID da tarefa selecionada
selected_task_id = None

# Função para abrir o GitHub ao clicar no botão de créditos
def open_github():
    webbrowser.open("https://github.com/lucascandev/")

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

# Função para carregar as tarefas na interface gráfica
def load_tasks(order_by="due_date"):
    global tasks  # Referência à variável global
    for widget in tasks_frame.winfo_children():
        widget.destroy()  # Limpa as tarefas anteriores do frame

    tasks = list_tasks(order_by)  # Carrega as tarefas do banco de dados

    for task in tasks:
        due_date = datetime.strptime(task[2], "%d/%m/%Y").strftime("%d/%m/%Y")
        task_str = f"ID: {task[0]} | {task[1]} | {due_date} | {task[3]} | {task[4]}"

        task_button = ctk.CTkButton(tasks_frame, text=task_str, command=lambda task_id=task[0]: select_task(task_id))
        task_button.pack(fill="x", padx=10, pady=5)

# Função para selecionar tarefa
def select_task(task_id):
    global selected_task_id
    selected_task_id = task_id  # Salva o ID da tarefa selecionada
    print(f"Tarefa {task_id} selecionada")  # Apenas para depuração

# Função para marcar tarefa como concluída
def mark_completed():
    global selected_task_id
    if selected_task_id is None:
        messagebox.showwarning("Seleção inválida", "Selecione uma tarefa para marcar como concluída.")
    else:
        mark_as_completed(selected_task_id)
        load_tasks()  # Atualiza a lista
        selected_task_id = None  # Limpa a seleção após a ação

# Função para excluir tarefa
def delete_task_gui():
    global selected_task_id
    if selected_task_id is None:
        messagebox.showwarning("Seleção inválida", "Selecione uma tarefa para excluir.")
    else:
        delete_task(selected_task_id)
        load_tasks()  # Atualiza a lista
        selected_task_id = None  # Limpa a seleção após a ação

# Função para mostrar gráficos das tarefas
def show_task_graphs():
    tasks = list_tasks()  # Carrega todas as tarefas

    # Contagem das tarefas por prioridade
    priority_counts = Counter([task[3] for task in tasks])
    priority_labels = list(priority_counts.keys())
    priority_values = list(priority_counts.values())

    # Gráfico de tarefas por prioridade
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.bar(priority_labels, priority_values, color='skyblue')
    ax.set_title("Tarefas por Prioridade")
    ax.set_xlabel("Prioridade")
    ax.set_ylabel("Quantidade de Tarefas")
    ax.set_ylim(0, max(priority_values) + 1)
    
    # Exibe o gráfico
    plt.show()

# Função de ordenação
def sort_by_priority():
    load_tasks(order_by="priority")

def sort_by_date():
    load_tasks(order_by="due_date")

# Criar janela principal com CustomTkinter
root = ctk.CTk()
root.title("Gestor de Tarefas")
root.geometry("800x700")  # Ajuste do tamanho da janela para mais adequado

# Seletor de prioridade
priority_label = ctk.CTkLabel(root, text="Selecione a Prioridade:")
priority_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

priority_combobox = ctk.CTkComboBox(root, values=["Alta", "Média", "Baixa"], state="readonly")
priority_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Seletor de data de vencimento
date_label = ctk.CTkLabel(root, text="Data de Vencimento:")
date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

cal_due_date = DateEntry(root, date_pattern="dd/mm/yyyy", width=100, state="normal")
cal_due_date.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Botões de ação
add_button = ctk.CTkButton(root, text="Adicionar Tarefa", command=add_task_gui)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

mark_button = ctk.CTkButton(root, text="Marcar como Concluída", command=mark_completed)
mark_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

delete_button = ctk.CTkButton(root, text="Excluir Tarefa", command=delete_task_gui)
delete_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Botão de exibir gráficos
graph_button = ctk.CTkButton(root, text="Mostrar Gráficos", command=show_task_graphs)
graph_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Frame para exibir as tarefas
tasks_frame = ctk.CTkFrame(root)
tasks_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=20, sticky="nsew")

# Ordenação de tarefas
sort_priority_button = ctk.CTkButton(root, text="Ordenar por Prioridade", command=sort_by_priority)
sort_priority_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

sort_date_button = ctk.CTkButton(root, text="Ordenar por Data", command=sort_by_date)
sort_date_button.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

# Botão de Créditos
credits_button = ctk.CTkButton(root, text="Créditos", command=open_github)
credits_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Carregar tarefas na interface
load_tasks()

# Iniciar o loop da interface gráfica
root.mainloop()
