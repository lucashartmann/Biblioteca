from textual.widgets import Input, Label, Button, Select
from textual.containers import Container, HorizontalGroup
from controller import Controller
from textual import on
from textual.message import Message


class CadastroRealizado(Message):
    def __init__(self, sender) -> None:
        super().__init__()
        self.sender = sender


class TelaCadastroLivro(Container):

    montou = False
    valor_select = ""

    def compose(self):
        yield Label("Codigo do Livro:", id="lb_id")
        yield Input(placeholder="Codigo aqui", id="input_id")
        yield Label("*Titulo:", id="lbl_titulo")
        yield Input(placeholder="Titulo aqui", id="inpt_titulo")
        yield Label("*Autor:", id="lbl_autor")
        yield Input(placeholder="Autor aqui", id="inpt_autor")
        yield Label("*Quantidade:", id="lbl_quant")
        yield Input(placeholder="Quantidade aqui", id="inpt_quant")
        yield Label("Caminho da Capa:")
        yield Input(placeholder="Caminho aqui")
        yield Input(placeholder="Largura aqui")
        yield Input(placeholder="Altura aqui")
        yield Select([("genero", 'genero')], id="slct_genero")
        yield HorizontalGroup(id="hg_genero")
        yield Select([("Cadastrar", 'Cadastrar'), ("Editar", "Editar"), ("Remover", "Remover")], id="select_operacao")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Executar", id="bt_executar")
        yield Button("Voltar", id="bt_voltar")

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:

            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_limpar":
                for input in self.query(Input):
                    input.value = ""
            case "bt_executar":
                match self.query_one("#select_operacao", Select).value:
                    case "Cadastrar":
                        if self.montou:
                            self.montou = False
                            self.query_one("#lbl_genero").remove()
                            self.query_one("#inpt_genero").remove()
                        self.cadastro()

                    case "Editar":                           
                        input_id = self.query_one("#input_id", Input).value
                        dados = []
                        for input in self.query(Input)[1:]:
                            dados.append(input.value.upper())
                        if self.valor_select != "Novo Genero":
                            if self.query_one("#slct_genero", Select).is_blank():
                                dados.append("")
                            else:
                                dados.append(self.query_one(
                                    "#slct_genero", Select).value)
                        elif self.montou:
                            dados.append(self.query_one(
                                "#inpt_genero", Input).value)
                            self.montou = False
                            self.query_one("#lbl_genero").remove()
                            self.query_one("#inpt_genero").remove()
                            
                        mensagem = Controller.editar_livro(input_id, dados)
                        self.notify(str(mensagem), markup=False)
                        self.on_mount()
                        self.post_message(CadastroRealizado(self))

                    case "Remover":
                        input_id = self.query_one(Input).value
                        mensagem = Controller.excluir_livro(input_id)
                        self.notify(str(mensagem), markup=False)
                        self.post_message(CadastroRealizado(self))
                        self.on_mount()

                    case _:
                        self.notify("Nenhuma opção de operação selecionada")

    montou = False
    valor_select = ""

    def on_mount(self):
        livros = Controller.get_livros_biblioteca().values()
        lista_generos = []
        for livro in livros:
            if livro.get_genero() not in lista_generos:
                lista_generos.append(livro.get_genero())
        if "Novo Genero" not in lista_generos:
            lista_generos.append("Novo Genero")
        select = self.query_one("#slct_genero", Select)
        select2 = self.query_one("#select_operacao", Select)
        select2.prompt = "Escolha operação"
        select.prompt = "Escolha genêro"
        select.set_options(
            [(genero, genero) for genero in lista_generos])

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        if evento.select.id == "slct_genero":
            self.valor_select = str(evento.value)
            hg = self.query_one("#hg_genero", HorizontalGroup)
            hg.styles.column_span = 2
            evento.select.styles.column_span = 2
            evento.select.styles.width = "40%"
            if self.valor_select == "Novo Genero" and not self.montou:
                hg.mount(Label("genero:", id="lbl_genero"))
                hg.mount(
                    Input(placeholder="genero aqui", id="inpt_genero"))
                self.montou = True
            elif self.valor_select != "Novo Genero" and self.montou:
                self.query_one("#lbl_genero").remove()
                self.query_one("#inpt_genero").remove()
                self.montou = False

    def cadastro(self):
        dados = []
        for input in self.query(Input)[1:]:
            dados.append(input.value.upper())
        if self.valor_select != "Novo Genero":
            if self.query_one("#slct_genero", Select).is_blank():
                dados.append("")
            else:
                dados.append(self.query_one("#slct_genero", Select).value)
        elif self.montou:
            dados.append(self.query_one("#inpt_genero", Input).value)
        else:
            dados.append("")
        resultado = Controller.cadastrar_livro(dados)
        self.notify(str(resultado), markup=False)
        self.on_mount()
        self.post_message(CadastroRealizado(self))
