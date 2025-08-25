from textual.widgets import Input, Label, Button, TabbedContent, TabPane, Select, Static
from textual.containers import Container, HorizontalGroup, VerticalScroll
from controller import Controller
from textual import on
from textual.message import Message


class CadastroRealizado(Message):
    def __init__(self, sender) -> None:
        super().__init__()
        self.sender = sender


class TelaCadastrar(Container):

    montou = False
    valor_select = ""

    def compose(self):
        yield Label("Titulo:", id="lbl_titulo")
        yield Input(placeholder="Titulo aqui", id="inpt_titulo")
        yield Label("Autor:", id="lbl_autor")
        yield Input(placeholder="Autor aqui", id="inpt_autor")
        yield Label("Quantidade:", id="lbl_quant")
        yield Input(placeholder="Quantidade aqui", id="inpt_quant")
        yield Select([("genero", 'genero')], id="slct_genero")
        yield HorizontalGroup(id="hg_genero")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Cadastrar", id="bt_cadastrar")
        yield Button("Voltar", id="bt_voltar")

    def cadastro(self):
        dados = []
        for input in self.query(Input):
            dados.append(input.value.upper())
        if self.valor_select != "Novo Genero":
            if self.query_one(Select).is_blank():
                dados.append("")
            else:
                dados.append(self.query_one(Select).value)
        elif self.montou:
            dados.append(self.query_one("#inpt_genero", Input).value)
        else:
            dados.append("")
        resultado = Controller.cadastrar_livro(dados)
        self.notify(str(resultado), markup=False)
        self.screen.on_mount()
        self.post_message(CadastroRealizado(self))

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_cadastrar":
            if self.montou:
                self.montou = False
                self.query_one("#lbl_genero").remove()
                self.query_one("#inpt_genero").remove()
            self.cadastro()


class TelaRemover(Container):
    def compose(self):
        yield Label("ID do Livro:", id="lb_id")
        yield Input(placeholder="ID aqui", id="input_id")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Remover", id="bt_remover")
        yield Button("Voltar", id="bt_voltar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_remover":
            input_id = self.query_one(Input).value
            mensagem = Controller.excluir_livro(input_id)
            self.notify(str(mensagem), markup=False)
            self.post_message(CadastroRealizado(self))


class TelaEditar(VerticalScroll):

    montou = False
    valor_select = ""

    def compose(self):
        yield Label("ID do Livro:")
        yield Input(placeholder="ID aqui", id="ipt_id")
        yield Label("Titulo:")
        yield Input(placeholder="Titulo aqui")
        yield Label("Autor:", id="lbl_autor")
        yield Input(placeholder="Autor aqui", id="inpt_autor")
        yield Label("Quantidade:", id="lbl_quant")
        yield Input(placeholder="Quantidade aqui", id="inpt_quant")
        yield Label("Caminho da Capa:")
        yield Input(placeholder="Caminho aqui")
        yield Input(placeholder="Largura aqui")
        yield Input(placeholder="Altura aqui")
        yield Select([("genero", 'genero')], id="slct_genero")
        yield HorizontalGroup(id="hg_genero")
        yield Button("Editar", id="bt_editar")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Voltar", id="bt_voltar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_editar":
            if self.montou:
                self.montou = False
                self.query_one("#lbl_genero").remove()
                self.query_one("#inpt_genero").remove()
            input_id = self.query_one("#ipt_id", Input).value
            dados = []
            for input in self.query(Input)[1:]:
                dados.append(input.value.upper())
            if self.valor_select != "Novo Genero":
                if self.query_one(Select).is_blank():
                    dados.append("")
                else:
                    dados.append(self.query_one(Select).value)
            elif self.montou:
                dados.append(self.query_one(
                    "#inpt_genero", Input).value)
            else:
                dados.append("")
            mensagem = Controller.editar_livro(input_id, dados)
            self.notify(str(mensagem), markup=False)
            self.screen.on_mount()
            self.post_message(CadastroRealizado(self))


class TelaCadastroLivro(Container):
    CSS_PATH = "css/TelaCadastroLivro.tcss"

    def compose(self):
        with TabbedContent():
            with TabPane("Cadastrar"):
                yield TelaCadastrar()
            with TabPane("Editar"):
                yield TelaEditar()
            with TabPane("Remover"):
                yield TelaRemover()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_limpar":
                for input in self.query(Input):
                    input.value = ""

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
        for select in self.query(Select):
            select.set_options(
                [(genero, genero) for genero in lista_generos])

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        self.valor_select = str(evento.value)
        select = evento._sender
        container = select.parent
        hg = container.query_one("#hg_genero", HorizontalGroup)
        hg.styles.column_span = 2
        select.styles.column_span = 2
        select.styles.width = "40%"
        if self.valor_select == "Novo Genero" and not self.montou:
            hg.mount(Label("genero:", id="lbl_genero"))
            hg.mount(
                Input(placeholder="genero aqui", id="inpt_genero"))
            self.montou = True
        elif self.valor_select != "Novo Genero" and self.montou:
            self.query_one("#lbl_genero").remove()
            self.query_one("#inpt_genero").remove()
            self.montou = False
