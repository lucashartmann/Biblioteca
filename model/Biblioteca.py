from model import Emprestimo


class Biblioteca:

    def __init__(self):
        self.nome = ""
        self.livros = dict()
        self.leitores = dict()

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
        return self.livros

    def get_lista_leitores(self):
        return self.leitores

    def get_livro_por_cod(self, cod_livro):
        if cod_livro in self.livros.keys():
            return self.livros[cod_livro]
        return None

    def get_leitor_por_email(self, email):
        if email in self.leitores.keys():
            return self.leitores[email]
        return None

    def add_livro(self, livro):
        if not self.get_livro_por_cod(livro.get_codigo()):
            self.livros[livro.get_codigo()] = livro
            return True
        return False

    def add_leitor(self, leitor):
        if not self.get_leitor_por_email(leitor.get_email()):
            self.leitores[leitor.get_email()] = leitor
            return True
        return False

    def remove_livro(self, cod_livro):
        if self.get_livro_por_cod(cod_livro):
            del self.livros[cod_livro]
            return True
        return False

    def remove_leitor(self, email):
        if self.get_leitor_por_email(email):
            del self.leitores[email]
            return True
        return False

    def __str__(self):
        return f"Biblioteca [Livros = {self.get_lista_livros()}, Leitores = {self.get_lista_leitores()}]"
