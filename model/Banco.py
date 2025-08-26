import sqlite3


class Banco:

    def __init__(self):
        self.conexao = sqlite3.connect('data/Biblioteca.db')
        self.cursor = self.conexao.cursor()

    def commit(self):
        self.conexao.commit()

    def close_cursor(self):
        self.cursor.close()

    def close_conection(self):
        self.conexao.close()

    def criar_tabela(self, nome_tabela):
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {nome_tabela} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        ''')

    def inserir_dados(self, dados, nome_tabela):
        self.cursor.executemany(
            f'INSERT INTO {nome_tabela} (nome, email) VALUES (?, ?)', dados)


    def consulta(self, dados):
        self.cursor.execute('SELECT * FROM usuarios WHERE email = ?', (dados,))
        return self.cursor.fetchone()


    def atualizar_tabela(self, dados, nome_tabela):
        sql_update_query = """
            UPDATE {nome_tabela}
            SET coluna1 = ?
            WHERE coluna2 = ?;
        """
        return True
        #dados = ('novo_valor', 'condicao')
