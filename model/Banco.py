

class Banco:

    def __init__(self):
       

    def salvar_alteracoes(self):
        

    def fechar_cursor(self, cursor):
        

    def encerrar_conexao(self):
        self.conexao.close()

    def criar_tabela(self, nome_tabela):
        cursor = self.get_cursor()

        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {nome_tabela} (
            nome VARCHAR(50),
            email VARCHAR(50) PRIMARY KEY
        )
        ''')

        self.salvar_alteracoes()
        self.fechar_cursor(cursor)
        # self.encerrar_conexao()
        return True

    def inserir_dados(self, lista_dados, nome_tabela):
       

    def consulta_dado(self, nome_tabela, dado):
        cursor = self.get_cursor()

        cursor.execute(f'SELECT * FROM {nome_tabela} WHERE email = ?', (dado,))

        registo = cursor.fetchone()

        if not registo:
            return None

        self.salvar_alteracoes()
        self.fechar_cursor(cursor)
        # self.encerrar_conexao()
        return registo
    
    def consultar_multiplos_dados(self, nome_tabela, tipo_dado, lista_dados, quant):
        cursor = self.get_cursor()
        
        placeholders = ', '.join(['?'] * len(lista_dados))  # Gera "?, ?, ?"

        query = f'SELECT * FROM {nome_tabela} WHERE {tipo_dado} IN ({placeholders})'

        cursor.execute(query, lista_dados)

        registros = cursor.fetchmany(quant)

        self.salvar_alteracoes()
        self.fechar_cursor(cursor)
        # self.encerrar_conexao()

        return registros


    def atualizar_tabela(self, nome_tabela, novo_valor, condicao):
        cursor = self.get_cursor()

        sql_update_query = f"""
            UPDATE {nome_tabela}
            SET coluna1 = {novo_valor}
            WHERE coluna2 = {condicao};
        """

        cursor.execute(sql_update_query)
        self.salvar_alteracoes()
        self.fechar_cursor(cursor)
        # self.encerrar_conexao()

        return True
