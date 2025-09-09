import sqlite3
import os
from model import Emprestimo, Livro, Leitor


class Banco:

    def __init__(self):
        diretorio = "data"
        if not os.path.isdir(diretorio):
            os.makedirs(diretorio)
        self.init_tabelas()

    def init_tabelas(self):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Leitor (
                    nome TEXT NOT NULL,
                    email TEXT PRIMARY KEY
                );
                ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Livro (
                    id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    capa Longblob NULL,
                    disponivel NOT NULL
                );
                ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Emprestimo (
                    id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_livro INTEGER NOT NULL,
                    email_leitor TEXT NOT NULL,
                    data_para_devolucao TEXT NOT NULL,
                    FOREIGN KEY (id_livro) REFERENCES Livro (id_livro),
                    FOREIGN KEY (email_leitor) REFERENCES Leitor (email)
                );
                ''')

            conexao.commit()

    def add_livro(self, livro):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute(
                    f'INSERT INTO Livro (titulo, autor, genero, quantidade, capa, disponivel) VALUES (?, ?, ?, ?, ?, ?)', (livro.get_titulo(), livro.get_autor(), livro.get_genero(), livro.get_quant(), livro.get_capa_binaria(), livro.is_disponivel()))
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao adicionar livro", e)
                return False

    def add_leitor(self, leitor):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute(
                    f'INSERT INTO Leitor (nome, email) VALUES (?, ?)', (leitor.get_nome(), leitor.get_email()))
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao adicionar leitor", e)
                return False

    def add_emprestimo(self, emprestimo):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            try:
                cursor.execute(
                    f'INSERT INTO Emprestimo (id_livro, email_leitor, data_para_devolucao) VALUES (?, ?, ?)', (int(emprestimo.get_livro().get_codigo()), emprestimo.get_leitor().get_email(), emprestimo.get_data_para_devolucao()))
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao adicionar empréstimo", e)
                return False

    def remove_livro(self, cod_livro):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            try:
                sql_delete_query = """
                    DELETE FROM Livro
                    WHERE id_livro = ?;
                    """
                cursor.execute(sql_delete_query, (cod_livro,))
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao remover livro", e)
                return False

    def remove_leitor(self, email):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            try:
                sql_delete_query = """
                    DELETE FROM Leitor
                    WHERE email = ?;
                    """
                cursor.execute(sql_delete_query, (email,))
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao remover leitor", e)
                return False

    def remove_emprestimo(self, id_emprestimo):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            try:
                sql_delete_query = """
                    DELETE FROM Emprestimo
                    WHERE id_emprestimo = ?;
                    """
                cursor.execute(sql_delete_query, (id_emprestimo,))
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao remover empréstimo", e)
                return False

    def get_emprestimo_por_livro(self, cod_livro):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                f'SELECT * FROM Emprestimo WHERE id_livro = ?', (cod_livro,))
            registro = cursor.fetchone()
            if not registro:
                return None
            livro = self.get_livro_por_cod(registro[1])
            leitor = self.get_leitor_por_email(registro[2])
            emprestimo = Emprestimo.Emprestimo(livro, leitor)
            emprestimo.set_id(registro[0])
            emprestimo.set_data_para_devolucao(registro[-1])
            return emprestimo

    def get_emprestimo_por_id(self, id_emprestimo):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                f'SELECT * FROM Emprestimo WHERE id_emprestimo = ?', (id_emprestimo,))
            registro = cursor.fetchone()
            if not registro:
                return None
            livro = self.get_livro_por_cod(registro[1])
            leitor = self.get_leitor_por_email(registro[2])
            emprestimo = Emprestimo.Emprestimo(livro, leitor)
            emprestimo.set_id(registro[0])
            emprestimo.set_data_para_devolucao(registro[-1])
            return emprestimo

    def get_emprestimos_por_leitor(self, email_leitor):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                f'SELECT * FROM Emprestimo WHERE email_leitor = ?', (email_leitor,))
            lista_registros = cursor.fetchall()
            lista_emprestimos = []
            for registro in lista_registros:
                livro = self.get_livro_por_cod(registro[1])
                leitor = self.get_leitor_por_email(registro[2])
                emprestimo = Emprestimo.Emprestimo(livro, leitor)
                emprestimo.set_id(registro[0])
                emprestimo.set_data_para_devolucao(registro[-1])
                lista_emprestimos.append(emprestimo)

            return lista_emprestimos

    def get_lista_emprestimos(self):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM Emprestimo")
            resultados = cursor.fetchall()
            for dados in resultados:
                livro = self.get_livro_por_cod(dados[1])
                leitor = self.get_leitor_por_email(dados[2])
                emprestimo = Emprestimo.Emprestimo(livro, leitor)
                emprestimo.set_id(dados[0])
                emprestimo.set_data_para_devolucao(dados[-1])
                lista.append(emprestimo)
            return lista

    def get_lista_livros(self):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM Livro")
            resultados = cursor.fetchall()
            for dados in resultados:
                livro = Livro.Livro(*dados[1:5])
                livro.set_codigo(dados[0])
                livro.set_capa_binaria(dados[5])
                if dados[-1] == 1:
                    livro.set_disponivel(True)
                else:
                    livro.set_disponivel(False)
                lista.append(livro)
            return lista

    def get_lista_leitores(self):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM Leitor")
            resultados = cursor.fetchall()
            for dados in resultados:
                lista.append(Leitor.Leitor(*dados))
            return lista

    def get_livro_por_cod(self, cod_livro):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Livro WHERE id_livro = ?', (cod_livro,))
            registro = cursor.fetchone()
            if not registro:
                return None
            livro = Livro.Livro(*registro[1:5])
            livro.set_codigo(registro[0])
            livro.set_capa_binaria(registro[5])
            if registro[-1] == 1:
                livro.set_disponivel(True)
            else:
                livro.set_disponivel(False)
            return livro

    def get_leitor_por_email(self, email):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(f'SELECT * FROM Leitor WHERE email = ?', (email,))
            registro = cursor.fetchone()
            if not registro:
                return None
            return Leitor.Leitor(*registro)

    def atualizar_livro(self, tipo_dado, condicao, novo_valor):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            try:
                sql_update_query = f"""
                UPDATE Livro
                SET {tipo_dado} = ?
                WHERE id_livro = ?;
                """
                dados = (novo_valor, condicao)
                cursor.execute(sql_update_query, dados)
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao atualizar livro", e)
                return False

    def atualizar_leitor(self, tipo_dado, condicao, novo_valor):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            try:
                sql_update_query = f"""
                UPDATE Leitor
                SET {tipo_dado} = ?
                WHERE email = ?;
                """
                dados = (novo_valor, condicao)
                cursor.execute(sql_update_query, dados)
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO ao atualizar leitor", e)
                return False
