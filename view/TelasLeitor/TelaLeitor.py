from textual.screen import Screen
from textual.widgets import TabbedContent, TabPane, Footer, Header
from view.TelasLeitor import TelaDevolucao
from view import TelaCadastroLeitor, TelaEstoque

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
        self.sub_title = "Tela Inicial"
