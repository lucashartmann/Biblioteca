from model import Emprestimo, Banco


class Biblioteca:
    
    def __init__(self):
        self.banco_dados = Banco.Banco()

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
        return self.banco_dados.get_lista_livros()

    def get_lista_leitores(self):
        return self.banco_dados.get_lista_leitores()

    def get_livro_por_cod(self, cod_livro):
        return self.banco_dados.get_livro_por_cod(cod_livro)

    def get_leitor_por_email(self, email):
       return self.banco_dados.get_leitor_por_email(email)

    def add_livro(self, livro):
       return self.banco_dados.add_livro(livro)

    def add_leitor(self, leitor):
       return self.banco_dados.add_leitor(leitor)

    def remove_livro(self, cod_livro):
       return self.banco_dados.remove_livro(cod_livro)

    def remove_leitor(self, email):
       return self.banco_dados.remove_leitor(email)
   
    def atualizar_livro(self, tipo_dado, condicao, novo_valor):
        return self.banco_dados.atualizar_livro(tipo_dado, condicao, novo_valor)

    def __str__(self):
        return f"Biblioteca [Livros = {self.get_lista_livros()}, Leitores = {self.get_lista_leitores()}]"

