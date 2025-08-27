class Leitor:

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self.emprestimos = list()

    def add_emprestimo(self, emprestimo):
        if emprestimo not in self.emprestimos:
            self.emprestimos.append(emprestimo)
            return True
        return False

    def remove_emprestimo(self, emprestimo):
        if emprestimo in self.emprestimos:
            self.emprestimos.remove(emprestimo)
            return True
        return False

    def get_emprestimo_por_livro(self, cod_livro):
        for emprestimo in self.emprestimos:
            if emprestimo.get_livro().get_codigo() == cod_livro:
                return emprestimo
        return None

    def get_emprestimo_por_id(self, id_emprestimo):
        for emprestimo in self.emprestimos:
            if emprestimo.get_id() == id_emprestimo:
                return emprestimo
        return None

    def get_lista_emprestimos(self):
        return self.emprestimos

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
