from textual.widgets import Input, Pretty, TextArea, Button, Select
from textual.containers import HorizontalGroup, VerticalScroll
from controller import Controller
from textual import on
from model import Init
from textual.message import Message


class RetiradaRealizada(Message):
    def __init__(self, sender) -> None:
        super().__init__()
        self.sender = sender


class TelaEstoque(VerticalScroll):

    def compose(self):
        with HorizontalGroup(id="hg_pesquisa"):
            yield Select([("genero", 'genero')])
            yield Input()
            if Init.usuario_leitor:
                yield Button("Retirar", id="bt_retirar")
            else:
                yield Button("Remover", id="bt_remover")
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(read_only=True)
        with HorizontalGroup(id="container"):
            pass

    livros = Controller.get_livros_biblioteca().values()

    livros_filtrados = []
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    montou = False

    def setup_dados(self):
        if len(self.livros_filtrados) > 0:
            quant = len(self.livros_filtrados)
        else:
            quant = len(self.livros)
        self.query_one(TextArea).text = f"Exemplo de busca: 'titulo: Maus - 1984, genero: distopia' \n\nQuantidade de livros: {quant}"

    def on_mount(self):
        emprestimos_str = []
        if self.montou:
            self.query_one(Pretty).update(emprestimos_str)
        else:
            self.mount(Pretty(emprestimos_str))
            self.montou = True
        self.atualizar()
        self.setup_dados()
        lista_categorias = []
        for livro in self.livros:
            if livro.get_genero() not in lista_categorias:
                lista_categorias.append(livro.get_genero())
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])
        self.query_one(Select).prompt = "Escolha genêro"

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_retirar":
                cod_livro = self.query_one(Input).value
                retirada = Controller.emprestar(
                    cod_livro, Init.leitor1.get_email())
                self.notify(retirada)
                self.on_mount()
                self.post_message(RetiradaRealizada(self))
            case "bt_remover":
                input_id = self.query_one(Input).value
                mensagem = Controller.excluir_livro(input_id)
                self.notify(str(mensagem), markup=False)
                self.on_mount()

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        if evento.select.is_blank():
            if self.filtrou_input == False and self.filtrou_select:
                self.livros_filtrados = []
            livros_str = [str(livro) for livro in self.livros]
            self.query_one(Pretty).update(livros_str)
            self.setup_dados()
            self.filtrou_select = False
        else:
            valor_select = str(evento.value)
            valor_antigo = ""
            if valor_select != valor_antigo and self.filtrou_input == False and self.filtrou_select:
                self.livros_filtrados = []
                valor_antigo = valor_select
            if len(self.livros_filtrados) == 0:
                for livro in self.livros:
                    if livro.get_genero() == valor_select:
                        self.livros_filtrados.append(livro)
            else:
                livros_temp = []
                for livro in self.livros_filtrados:
                    if livro.get_genero() == valor_select:
                        livros_temp.append(livro)
                if len(livros_temp) > 0:
                    self.livros_filtrados = livros_temp

            livros_str = [str(livro)for livro in self.livros_filtrados]
            self.query_one(Pretty).update(livros_str)
            self.setup_dados()
            self.filtrou_select = True
            self.select_evento = evento

    def filtro(self, palavras, index, filtro_recebido):
        lista_filtros = ["quant", "codigo"]
        campo = f"get_{filtro_recebido}"
        nova_lista = []

        if index + 1 < len(palavras):
            filtro = " ".join((palavras[index+1:]))

            if "," in filtro:
                filtro = filtro[0:filtro.index(
                    ",")]
            if "-" in filtro.split():
                for palavraa in filtro.split("-"):
                    if filtro.index("-")+1 < len(filtro) and palavraa not in nova_lista:
                        nova_lista.append(palavraa.strip())

            if filtro_recebido in lista_filtros:
                try:
                    filtro = int(filtro)
                except ValueError:
                    self.notify("Valor Inválido")
                    return

            if len(self.livros_filtrados) > 0:
                livros_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for livro in self.livros_filtrados:
                            if type(filtro) == int:
                                if p == getattr(livro, campo)() and livro not in livros_temp:
                                    livros_temp.append(
                                        livro)
                            else:
                                if p in getattr(livro, campo)() and livro not in livros_temp:
                                    livros_temp.append(
                                        livro)
                else:
                    for livro in self.livros_filtrados:
                        if type(filtro) == int:
                            if filtro == getattr(livro, campo)() and livro not in livros_temp:
                                livros_temp.append(livro)
                        else:
                            if filtro in getattr(livro, campo)() and livro not in livros_temp:
                                livros_temp.append(livro)
                if len(livros_temp) > 0:
                    self.livros_filtrados = livros_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for livro in self.livros:
                            if type(filtro) == int:
                                if p == getattr(livro, campo)() and livro not in self.livros_filtrados:
                                    self.livros_filtrados.append(
                                        livro)
                            else:
                                if p in getattr(livro, campo)() and livro not in self.livros_filtrados:
                                    self.livros_filtrados.append(
                                        livro)
                else:
                    for livro in self.livros:
                        if type(filtro) == int:
                            if filtro == getattr(livro, campo)() and livro not in self.livros_filtrados:
                                self.livros_filtrados.append(livro)
                        else:
                            if filtro in getattr(livro, campo)() and livro not in self.livros_filtrados:
                                self.livros_filtrados.append(livro)

    def atualizar(self):
        resultado = self.query_one(Pretty)
        livros_str = []
        lista = self.livros
        if len(self.livros_filtrados) > 0:
            lista = self.livros_filtrados

        if Init.usuario_leitor:
            lista_usuario = []
            for livro in lista:
                if livro.is_disponivel():
                    lista_usuario.append(livro)
            lista = lista_usuario
            for livro in lista:
                if livro.is_disponivel():
                    livro_str = str(livro).split(",")[:-1]
                    livros_str.append(livro_str)
        else:
            livros_str = [str(livro) for livro in lista]
        self.setup_dados()
        resultado.update(livros_str)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        palavras = texto.split()

        if len(palavras) > 0:
            if self.filtrou_select == False:
                self.livros_filtrados = []

            for palavra in palavras:
                match palavra:

                    case "GENERO:":
                        index = palavras.index("GENERO:")
                        self.filtro(palavras, index, "genero")

                    case "TITULO:":
                        index = palavras.index("TITULO:")
                        self.filtro(palavras, index, "titulo")

                    case "QUANTIDADE:":
                        index = palavras.index("QUANTIDADE:")
                        self.filtro(palavras, index, "quant")

                    case  "AUTOR:":
                        index = palavras.index("AUTOR:")
                        self.filtro(palavras, index, "autor")

                    case "CODIGO:":
                        index = palavras.index("CODIGO:")
                        self.filtro(palavras, index, "codigo")

                self.atualizar()
        else:
            if self.filtrou_select == False:
                self.atualizar()
            elif self.filtrou_select:
                self.select_changed(self.select_evento)
