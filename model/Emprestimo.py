import datetime
import random


class Emprestimo:
    id = 0

    def __init__(self, livro, leitor):
        self.livro = livro
        self.leitor = leitor
        self.data_para_devolucao = self.calcular_data_para_devolucao()
        self.id = self.gerar_id()

    def gerar_id(self):
        Emprestimo.id += 1
        return Emprestimo.id

    def get_id(self):
        return self.id

    def get_livro(self):
        return self.livro

    def get_leitor(self):
        return self.leitor

    def get_data_para_devolucao(self):
        return self.data_para_devolucao

    def set_livro(self, novo_livro):
        self.livro = novo_livro

    def set_leitor(self, novo_leitor):
        self.leitor = novo_leitor

    def set_data_para_devolucao(self, nova_data):
        self.data_para_devolucao = nova_data

    def calcular_data_para_devolucao(self):
        hoje = datetime.date.today()
        prazo = datetime.timedelta(weeks=random.randint(1, 50))
        data_para_devolucao = hoje + prazo
        data_formatada = data_para_devolucao.strftime("%d/%m/%Y")
        return data_formatada

    def __str__(self):
        return f"Emprestimo [ID = {self.get_id()}, Livro = {self.get_livro().__str__().split(',')[:-2]}, Leitor = {self.get_leitor()}, Data para Devolução = {self.get_data_para_devolucao()}]"
