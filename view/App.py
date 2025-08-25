from textual.app import App
from view import TelaInicial, TelaEstoqueCapas
from view.TelasLeitor import TelaLeitor
from view.TelasAdmin import TelaAdmin
from textual.binding import Binding
from model import Shelve, Init

class App(App):

    
    BINDINGS = {
        Binding("s", "app.push_screen('tela_estoque')", "Tela Estoque"),
        Binding("ctrl+s", "salvar", "Salvar")
    }
        
    def action_salvar(self):
        mensagem = ""
        if Init.usuario_leitor:
            Shelve.salvar("Banco.db", "Leitor", Init.leitor1)
            mensagem += "Leitor salvo com sucesso"
        else:
            Shelve.salvar("Banco.db", "Biblioteca", Init.biblioteca)
            mensagem += "Biblioteca salva com sucesso"
        self.notify(mensagem)

    SCREENS = {
        "tela_inicial": TelaInicial.TelaInicial,
        "tela_admin": TelaAdmin.TelaAdmin,
        "tela_leitor": TelaLeitor.TelaLeitor,
        "tela_estoque": TelaEstoqueCapas.TelaEstoqueCapas
    }
    
    def on_mount(self):
        self.title = "Biblioteca"
        self.push_screen("tela_inicial")
