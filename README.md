# Gestor de Tarefas

Este é um simples **Gestor de Tarefas** desenvolvido com **Python** utilizando a biblioteca `tkinter` para a interface gráfica, `sqlite3` para o banco de dados e `matplotlib` para exibição de gráficos sobre as tarefas. Ele permite que você adicione, edite, exclua e visualize suas tarefas, além de mostrar gráficos sobre as tarefas por prioridade.

## Funcionalidades

- **Adicionar tarefas**: Insira uma descrição, data de vencimento e prioridade para criar uma nova tarefa.
- **Exibir tarefas**: Visualize todas as tarefas ordenadas por data ou prioridade.
- **Marcar como concluída**: Marque uma tarefa como concluída, movendo-a para o status "concluída".
- **Excluir tarefas**: Remova tarefas do sistema.
- **Exibir gráficos**: Veja gráficos sobre a distribuição das tarefas por prioridade.
- **Notificações de tarefas vencidas**: Receba notificações sobre tarefas que estão vencidas.

## Pré-requisitos

- **Python 3.x**: Este software foi desenvolvido utilizando Python 3.x.
- **Bibliotecas necessárias**: As bibliotecas externas necessárias são:
  - `customtkinter`
  - `tkcalendar`
  - `matplotlib`

Essas bibliotecas podem ser instaladas via `pip`.

## Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/lucascandev/task-manager.git
   cd task-manager
   ```