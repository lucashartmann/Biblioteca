from textual.screen import Screen
from textual.widgets import TabbedContent, TabPane, Footer, Header
from view.TelasAdmin import TelaCadastroLivro, TelaClientela
from view import TelaCadastroLeitor, TelaEstoque, TelaEstoqueCapas


class TelaAdmin(Screen):

    CSS_PATH = "css/TelaAdmin.tcss"

    def compose(self):
        yield Header()
        with TabbedContent():
            with TabPane("Cadastrar Livro"):
                yield TelaCadastroLivro.TelaCadastroLivro()
            with TabPane("Cadastrar Leitor"):
                yield TelaCadastroLeitor.TelaCadastroLeitor()
            with TabPane("Estoque"):
                yield TelaEstoque.TelaEstoque()
            with TabPane("Clientela"):
                yield TelaClientela.TelaClientela()
        yield Footer()
        
    def on_cadastro_realizado(self):
        tela_estoque = self.query_one(TelaEstoque.TelaEstoque)
        tela_estoque.on_mount()

    def on_cadastro_leitor_realizado(self):
        tela_clientela = self.query_one(TelaClientela.TelaClientela)
        tela_clientela.on_mount()

    def on_mount(self):
        self.sub_title = "Tela Inicial"

    def on_cadastro_leitor_realizado(self):
        tela_clientela = self.query_one(TelaClientela.TelaClientela)
        tela_clientela.on_mount()

    def on_mount(self):
        self.sub_title = "Tela Inicial"
