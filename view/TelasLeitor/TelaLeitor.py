from textual.screen import Screen
from textual.widgets import TabbedContent, TabPane, Footer, Header
from view.TelasLeitor import TelaDevolucao
from view import TelaCadastroLeitor, TelaEstoque
from view.TelasAdmin import TelaClientela

class TelaLeitor(Screen):

    CSS_PATH = "css/TelaLeitor.tcss"

    def compose(self):
        yield Header()
        with TabbedContent():
            with TabPane("Retirar Livro"):
                yield TelaEstoque.TelaEstoque()
            with TabPane("Devolver Livro"):
                yield TelaDevolucao.TelaDevolucao()
            with TabPane("Se Cadastrar"):
                yield TelaCadastroLeitor.TelaCadastroLeitor()
        yield Footer()

    def on_mount(self):
        self.sub_title = "Tela Leitor"

    def on_devolucao_realizada(self):
        tela_estoque = self.query_one(TelaEstoque.TelaEstoque)
        tela_estoque.on_mount()
      
    def on_retirada_realizada(self):
        tela_devolucao = self.query_one(TelaDevolucao.TelaDevolucao)
        tela_devolucao.on_mount()
        tela_estoque = self.query_one(TelaEstoque.TelaEstoque)
        tela_estoque.on_mount()
        
        
    def on_cadastro_realizado(self):
        tela_clientela = self.query_one(TelaClientela.TelaClientela)
        tela_clientela.on_mount()
     