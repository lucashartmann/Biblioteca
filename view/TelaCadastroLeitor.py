from textual.widgets import Input, Label, Button, Select
from textual.containers import Container
from controller import Controller
from model import Init
from textual.message import Message


class CadastroLeitorRealizado(Message):
    def __init__(self, sender) -> None:
        super().__init__()
        self.sender = sender


class TelaCadastroLeitor(Container):

    def compose(self):
        yield Label("Email do Leitor:")
        yield Input(placeholder="Email aqui", id="input_pesquisar_email")
        yield Label("Nome:")
        yield Input(placeholder="Nome aqui")
        yield Label("Email:")
        yield Input(placeholder="Email aqui", id="input_email")
        yield Select([("Cadastrar", 'Cadastrar'), ("Editar", "Editar"), ("Remover", "Remover")])
        yield Button("Limpar", id="bt_limpar")
        yield Button("Executar", id="bt_executar")
        yield Button("Voltar", id="bt_voltar")

    def on_mount(self):
        input_email = self.query_one("#input_pesquisar_email", Input)
        if Init.usuario_leitor:
            input_email.value = Init.leitor1.get_email()
            input_email.disabled = True
        else:
            input_email.value = ""
            input_email.disabled = False

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_limpar":
                for input in self.query(Input):
                    input.value = ""
            case "bt_executar":
                match self.query_one(Select).value:
                    case "Remover":
                        input_email = self.query_one(
                            "#input_pesquisar_email", Input).value
                        mensagem = Controller.excluir_leitor(
                            input_email.upper())
                        self.notify(str(mensagem), markup=False)
                        self.post_message(CadastroLeitorRealizado(self))
                    case "Editar":
                        input_email = self.query_one(
                            "#input_pesquisar_email", Input).value
                        dados = []
                        for input in self.query(Input)[1:]:
                            dados.append(input.value.upper())
                        mensagem = Controller.editar_leitor(
                            input_email.upper(), dados)
                        self.notify(str(mensagem), markup=False)
                        self.post_message(CadastroLeitorRealizado(self))
                    case "Cadastrar":
                        self.cadastro()
                    case _:
                        self.notify("Nenhuma opção de operação selecionada")

    def cadastro(self):
        dados = []
        for input in self.query(Input)[1:]:
            dados.append(input.value.upper())
        resultado = Controller.cadastrar_leitor(dados)
        self.notify(str(resultado), markup=False)
        self.post_message(CadastroLeitorRealizado(self))
