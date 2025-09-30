from textual.app import App
from view import TelaInicial, TelaEstoqueCapas
from view.TelasLeitor import TelaLeitor
from view.TelasAdmin import TelaAdmin
from textual.binding import Binding

class App(App):

    BINDINGS = {
        Binding("ctrl+l", "switch_screen('tela_estoque')", "Tela Estoque"),
    }

    SCREENS = {
        "tela_inicial": TelaInicial.TelaInicial,
        "tela_admin": TelaAdmin.TelaAdmin,
        "tela_leitor": TelaLeitor.TelaLeitor,
        "tela_estoque": TelaEstoqueCapas.TelaEstoqueCapas
    }

    def on_mount(self):
        self.title = "Biblioteca"
        self.push_screen("tela_inicial")
