from model.Banco import Banco


class Leitor:

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self.banco_dados = Banco()

    def fechar_banco(self):
        self.banco_dados.encerrar()

    def add_emprestimo(self, emprestimo):
        return self.banco_dados.add_emprestimo(emprestimo)

    def remove_emprestimo(self, emprestimo):
        return self.banco_dados.remove_emprestimo(emprestimo.get_id())

    def get_emprestimo_por_livro(self, cod_livro):
        return self.banco_dados.get_emprestimo_por_livro(cod_livro)

    def get_emprestimo_por_id(self, id_emprestimo):
        return self.banco_dados.get_emprestimo_por_id(id_emprestimo)

    def get_lista_emprestimos(self):
        return self.banco_dados.get_emprestimos_por_leitor(self.email)

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def set_nome(self, novo_nome):
        self.nome = novo_nome

    def set_email(self, novo_email):
        self.email = novo_email

    def __str__(self):
        return f"Leitor [Nome = {self.get_nome()}, Email = {self.get_email()}]"
