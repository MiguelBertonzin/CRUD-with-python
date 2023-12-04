import tkinter as tk
from tkinter import messagebox
import mysql.connector

class AplicacaoCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface CRUD")

        # Conectar ao banco de dados
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='master',
            database='trabalho',
        )
        self.cursor = self.conexao.cursor()

        # Tela de Seleção de Tabela
        self.selecionar_tabela()

    def selecionar_tabela(self):
        selecionar_tabela_toplevel = tk.Toplevel(self.root)
        selecionar_tabela_toplevel.title("Selecionar Tabela")

        tk.Label(selecionar_tabela_toplevel, text="Escolha a Tabela:").pack()


        opcoes_tabelas = ["transmissao", "patrocinios", "torcidas"]
        escolha_var = tk.StringVar()
        escolha_var.set(opcoes_tabelas[0])  # Valor padrão

        opcoes_menu = tk.OptionMenu(selecionar_tabela_toplevel, escolha_var, *opcoes_tabelas)
        opcoes_menu.pack(pady=10)

        btn_confirmar = tk.Button(selecionar_tabela_toplevel, text="Confirmar", command=lambda: self.abrir_tela_operacoes(escolha_var.get(), selecionar_tabela_toplevel))
        btn_confirmar.pack()

    def abrir_tela_operacoes(self, tabela, toplevel):
        toplevel.destroy()

        operacoes_toplevel = tk.Toplevel(self.root)
        operacoes_toplevel.title(f"Operações CRUD - Tabela {tabela.capitalize()}")

        # Botões de Operações
        btn_inserir = tk.Button(operacoes_toplevel, text="Inserir", command=lambda: self.inserir_tela(tabela))
        btn_inserir.pack(pady=10)

        btn_selecionar = tk.Button(operacoes_toplevel, text="Selecionar", command=lambda: self.selecionar_tela(tabela))
        btn_selecionar.pack(pady=10)

        btn_atualizar = tk.Button(operacoes_toplevel, text="Atualizar", command=lambda: self.atualizar_tela(tabela))
        btn_atualizar.pack(pady=10)

        btn_deletar = tk.Button(operacoes_toplevel, text="Deletar", command=lambda: self.deletar_tela(tabela))
        btn_deletar.pack(pady=10)

    def inserir_tela(self, tabela):
        # Lógica para a tela de inserção
        inserir_toplevel = tk.Toplevel(self.root)
        inserir_toplevel.title(f"Inserir Registro - Tabela {tabela.capitalize()}")

        # Obtendo os nomes das colunas da tabela selecionada
        self.cursor.execute(f"SHOW COLUMNS FROM {tabela}")
        colunas = [coluna[0] for coluna in self.cursor.fetchall()]

        entry_values = []  # Lista para armazenar os objetos Entry

        for coluna in colunas:
            tk.Label(inserir_toplevel, text=f"{coluna.capitalize()} ({tabela.capitalize()}):").pack()
            entry = tk.Entry(inserir_toplevel)
            entry.pack()
            entry_values.append(entry)

        btn_confirmar = tk.Button(inserir_toplevel, text="Confirmar", command=lambda: self.inserir_registro(tabela, colunas, [entry.get() for entry in entry_values], inserir_toplevel))
        btn_confirmar.pack()

    def inserir_registro(self, tabela, colunas, valores, toplevel):
        # Lógica para Inserir
        valores_formatados = ", ".join([f"'{valor}'" for valor in valores])
        comando = f'INSERT INTO {tabela} ({", ".join(colunas)}) VALUES ({valores_formatados})'
        try:
            self.cursor.execute(comando)
            self.conexao.commit()
            messagebox.showinfo("Inserir", f"Operação de Inserção realizada com sucesso! Tabela: {tabela}")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro no MySQL", f"Erro: {err}")
        toplevel.destroy()

    def selecionar_tela(self, tabela):
        # Lógica para a tela de seleção
        selecionar_toplevel = tk.Toplevel(self.root)
        selecionar_toplevel.title(f"Selecionar Registro - Tabela {tabela.capitalize()}")

        tk.Label(selecionar_toplevel, text=f"ID do {tabela.capitalize()} a ser Selecionado (ou 'listar' para listar todos):").pack()
        id_entry = tk.Entry(selecionar_toplevel)
        id_entry.pack()

        btn_confirmar = tk.Button(selecionar_toplevel, text="Confirmar", command=lambda: self.selecionar_registro(tabela, id_entry.get()))
        btn_confirmar.pack()

    def selecionar_registro(self, tabela, id_registro):
        # Lógica para Selecionar
        if id_registro.lower() == 'listar':
            self.listar_registros(tabela)
        else:
            comando = f'SELECT * FROM {tabela} WHERE id{tabela.capitalize()} = {id_registro}'
            self.cursor.execute(comando)
            resultado = self.cursor.fetchall()
            messagebox.showinfo("Selecionar", f"Resultado:\n{resultado}")

    def listar_registros(self, tabela):
        # Lógica para Listar todos os registros
        comando = f'SELECT * FROM {tabela}'
        self.cursor.execute(comando)
        resultado = self.cursor.fetchall()
        messagebox.showinfo("Listar Registros", f"Todos os registros na tabela {tabela}:\n{resultado}")

    def atualizar_tela(self, tabela):
        # Lógica para a tela de atualização
        atualizar_toplevel = tk.Toplevel(self.root)
        atualizar_toplevel.title(f"Atualizar Registro - Tabela {tabela.capitalize()}")

        tk.Label(atualizar_toplevel, text=f"ID do {tabela.capitalize()} a ser Atualizado:").pack()
        id_entry = tk.Entry(atualizar_toplevel)
        id_entry.pack()

        # Obtendo os nomes das colunas da tabela selecionada
        self.cursor.execute(f"SHOW COLUMNS FROM {tabela}")
        colunas = [coluna[0] for coluna in self.cursor.fetchall()]

        entry_values = []  # Lista para armazenar os objetos Entry

        for coluna in colunas:
            tk.Label(atualizar_toplevel, text=f"Novo {coluna.capitalize()} ({tabela.capitalize()}):").pack()
            entry = tk.Entry(atualizar_toplevel)
            entry.pack()
            entry_values.append(entry)

        btn_confirmar = tk.Button(atualizar_toplevel, text="Confirmar", command=lambda: self.atualizar_registro(tabela, colunas, id_entry.get(), [entry.get() for entry in entry_values], atualizar_toplevel))
        btn_confirmar.pack()

    def atualizar_registro(self, tabela, colunas, id_registro, novos_valores, toplevel):
        # Lógica para Atualizar
        set_clause = ", ".join([f"{coluna} = '{valor}'" for coluna, valor in zip(colunas, novos_valores)])
        comando = f'UPDATE {tabela} SET {set_clause} WHERE id{tabela.capitalize()} = {id_registro}'
        try:
            self.cursor.execute(comando)
            self.conexao.commit()
            messagebox.showinfo("Atualizar", f"Operação de Atualização realizada com sucesso! Tabela: {tabela}")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro no MySQL", f"Erro: {err}")
        toplevel.destroy()

    def deletar_tela(self, tabela):
        # Lógica para a tela de deleção 
        deletar_toplevel = tk.Toplevel(self.root)
        deletar_toplevel.title(f"Deletar Registro - Tabela {tabela.capitalize()}")

        tk.Label(deletar_toplevel, text=f"ID do {tabela.capitalize()} a ser Deletado:").pack()
        id_entry = tk.Entry(deletar_toplevel)
        id_entry.pack()

        btn_confirmar = tk.Button(deletar_toplevel, text="Confirmar", command=lambda: self.deletar_registro(tabela, id_entry.get(), deletar_toplevel))
        btn_confirmar.pack()

    def deletar_registro(self, tabela, id_registro, toplevel):
        # Lógica para Deletar
        comando = f'DELETE FROM {tabela} WHERE id{tabela.capitalize()} = {id_registro}'
        try:
            self.cursor.execute(comando)
            self.conexao.commit()
            messagebox.showinfo("Deletar", f"Operação de Deleção realizada com sucesso! Tabela: {tabela}")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro no MySQL", f"Erro: {err}")
        toplevel.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoCRUD(root)
    root.mainloop()
