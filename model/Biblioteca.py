import sqlite3
import os
import sys
from model import Emprestimo, Livro, Leitor


class Biblioteca:

    # self.encerrar_conexao()

    def __init__(self):
        e_exe, caminho = self.is_pyinstaller()
        if e_exe:
            self.conexao = sqlite3.connect(f"{caminho}\\data/Biblioteca.db")
        else:
            self.conexao = sqlite3.connect(f"data/Biblioteca.db")
        self.init_tabelas()
        self.nome = ""

    def is_pyinstaller(self):
        if getattr(sys, 'frozen', False):
            base_path = getattr(
                sys, '_MEIPASS', os.path.dirname(sys.executable))
            return True, base_path
        else:
            return False, ""

    def init_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS Leitor (
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) PRIMARY KEY
        )
        ''')

        self.conexao.commit()

        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS Livro (
            id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo VARCHAR NOT NULL, 
            autor VARCHAR NOT NULL, 
            genero VARCHAR NOT NULL, 
            quantidade INT NOT NULL,
            caminho_capa NULL, 
            largura_capa NULL,
            altura_capa NULL,
            disponivel NOT NULL
        )
        ''')

        cursor.execute(f'''
        CREATE TABLE Emprestimo (
            id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            email_leitor VARCHAR(50) NOT NULL,
            data_para_devolucao DATE NOT NULL,
            FOREIGN KEY (id_livro) REFERENCES Livro(id_livro),
            FOREIGN KEY (email_leitor) REFERENCES Leitor(email)
        );
        ''')

        self.conexao.commit()
        cursor.close()

    def emprestar(self, livro, leitor):
        if livro.is_disponivel():
            livro.set_quant(livro.get_quant() - 1)
            livro.atualizar_disponivel()
            return Emprestimo.Emprestimo(livro, leitor)
        return None

    def devolver(self, emprestimo):
        leitor = emprestimo.get_leitor()
        livro = emprestimo.get_livro()
        livro.set_quant(emprestimo.get_livro().get_quant() + 1)
        livro.atualizar_disponivel()
        leitor.remove_emprestimo(emprestimo)
        if not self.get_livro_por_cod(livro.get_codigo()):
            self.add_livro(livro)
        return True

    def get_lista_livros(self):
        lista = []
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM Livro")
        resultados = cursor.fetchall()
        cursor.close()
        if not resultados:
            return None
        for dados in resultados:
            livro = Livro.Livro(*dados[1:5])
            livro.set_caminho_capa(dados[5])
            livro.set_largura_capa(dados[6])
            livro.set_altura_capa(dados[7])
            livro.set_disponivel(dados[8])
            lista.append(livro)
        return lista

    def get_lista_leitores(self):
        lista = []
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM Leitor")
        resultados = cursor.fetchall()
        cursor.close()
        if not resultados:
            return None
        for dados in resultados:
            lista.append(Leitor.Leitor(*dados))
        return lista

    def get_livro_por_cod(self, cod_livro):
        cursor = self.conexao.cursor()
        cursor.execute(f'SELECT * FROM Livro WHERE id_livro = ?', (cod_livro,))
        registo = cursor.fetchone()
        if not registo:
            return None

        livro = Livro.Livro(*registo[1:5])
        livro.set_codigo(registo[0])
        livro.set_caminho_capa(registo[5])
        livro.set_largura_capa(registo[6])
        livro.set_altura_capa(registo[7])
        livro.set_disponivel(registo[8])

        cursor.close()
        return livro

    def get_leitor_por_email(self, email):
        cursor = self.conexao.cursor()
        cursor.execute(f'SELECT * FROM Leitor WHERE email = ?', (email,))
        registo = cursor.fetchone()
        if not registo:
            return None
        cursor.close()
        return Leitor.Leitor(*registo)

    def add_livro(self, livro):
        try:
            cursor = self.conexao.cursor()
            cursor.executemany(
                f'INSERT INTO Livro (titulo, autor, genero, quantidade, caminho_capa, largura_capa, altura_capa, disponivel) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [(livro.get_titulo(), livro.get_autor(), livro.get_genero(), livro.get_quant(), livro.get_caminho_capa(), livro.get_largura_capa(), livro.get_altura_capa(), livro.is_disponivel())])
            self.conexao.commit()
            cursor.close()
            return True
        except:
            return False

    def add_leitor(self, leitor):
        try:
            cursor = self.conexao.cursor()
            cursor.executemany(
                f'INSERT INTO Leitor (nome, email) VALUES (?, ?)', [(leitor.get_nome(), leitor.get_email())])
            self.conexao.commit()
            cursor.close()
            return True
        except:
            return False

    def remove_livro(self, cod_livro):
        try:
            cursor = self.conexao.cursor()
            sql_delete_query = """
            DELETE FROM Livro
            WHERE coluna1 = ?;
            """
            cursor.execute(sql_delete_query, cod_livro)
            self.conexao.commit()
            cursor.close()
            return True
        except:
            return False

    def remove_leitor(self, email):
        try:
            cursor = self.conexao.cursor()
            sql_delete_query = """
            DELETE FROM Leitor
            WHERE coluna1 = ?;
            """
            cursor.execute(sql_delete_query, email)
            self.conexao.commit()
            cursor.close()
            return True
        except:
            return False

    def __str__(self):
        return f"Biblioteca [Livros = {self.get_lista_livros()}, Leitores = {self.get_lista_leitores()}]"
