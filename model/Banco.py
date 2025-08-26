import sqlite3

class Banco:
    
    def __init__(self):
        self.conexao = sqlite3.connect('data/Biblioteca.db')
        self.cursor = self.conexao.cursor()
        
    def criar_tabela(self, nome_tabela):
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {nome_tabela} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        ''')
        self.conexao.commit()
        self.cursor.close()
        self.conexao.close()

    def inserir_dados(self, dados):
        self.cursor.executemany('INSERT INTO usuarios (nome, email) VALUES (?, ?)', dados)
        self.conexao.commit()

        self.cursor.close()
        self.conexao.close()
    
    def consulta(self, dados):
        self.cursor.execute('SELECT * FROM usuarios WHERE email = ?', (dados,))
        
        self.cursor.close()
        self.conexao.close()
