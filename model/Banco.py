import sqlite3

class Banco:

    conexao = sqlite3.connect('data/Biblioteca.db')

    cursor = conexao.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    conexao.commit()

    dados = [
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Carol', 'carol@example.com'),
        ('David', 'david@example.com'),
        ('Eve', 'eve@example.com'),
        ('Frank', 'frank@example.com'),
        ('Grace', 'grace@example.com'),
        ('Hank', 'hank@example.com'),
        ('Ivy', 'ivy@example.com'),
        ('Jack', 'jack@example.com')
    ]
    cursor.executemany('INSERT INTO usuarios (nome, email) VALUES (?, ?)', dados)
    conexao.commit()

    cursor.close()
    conexao.close()