from textual.app import App
from view import TelaInicial, TelaEstoqueCapas
from view.TelasLeitor import TelaLeitor
from view.TelasAdmin import TelaAdmin
from textual.binding import Binding
from controller import Controller

class App(App):

    
    BINDINGS = {
        Binding("ctrl+l", "switch_screen('tela_estoque')", "Tela Estoque"),
        Binding("ctrl+q", "sair", "Sair")
    }
    
    def action_sair(self):
        Controller.fechar_banco()
        self.exit()

    SCREENS = {
        "tela_inicial": TelaInicial.TelaInicial,
        "tela_admin": TelaAdmin.TelaAdmin,
        "tela_leitor": TelaLeitor.TelaLeitor,
        "tela_estoque": TelaEstoqueCapas.TelaEstoqueCapas
    }
    
    def on_mount(self):
        self.title = "Biblioteca"
        self.push_screen("tela_inicial")
