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
    CSS_PATH = "css/TelaEstoque.tcss"

    def compose(self):
        with HorizontalGroup(id="hg_pesquisa"):
            yield Select([("genero", 'genero')])
            yield Input()
            if Init.usuario_leitor:
                yield Button("Retirar", id="bt_retirar")
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        with HorizontalGroup(id="container"):
            pass

    livros = Controller.get_livros_biblioteca().values()

    livros_filtrados = []
    filtrou_checkbox = False
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    montou = False

    def setup_dados(self):
        if len(self.livros_filtrados) > 0:
            quant = len(self.livros_filtrados)
        else:
            quant = len(self.livros)
        self.query_one(TextArea).text = f"Quantidade de livros: {quant}"

    def on_mount(self):
        livros_str = []
        if Init.usuario_leitor:
            lista_usuario = []
            for livro in self.livros:
                if livro.is_disponivel():
                    lista_usuario.append(livro)
            self.livros = lista_usuario
        if Init.usuario_leitor:
            for livro in self.livros:
                if livro.is_disponivel():
                    livro_str = str(livro).split(",")[:-1]
                    livros_str.append(livro_str)
        else:
            livros_str = [str(livro) for livro in self.livros]
        if self.montou:
            self.query_one(Pretty).update(livros_str)
        else:
            self.mount(Pretty(livros_str))
            self.montou = True
        self.setup_dados()
        lista_categorias = []
        for livro in self.livros:
            if livro.get_genero() not in lista_categorias:
                lista_categorias.append(livro.get_genero())
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])

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

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        resultado = self.query_one(Pretty)
        palavras = texto.split()

        if len(palavras) > 0:
            if self.filtrou_select == False:
                self.livros_filtrados = []

            for palavra in palavras:
                match palavra:

                    case "GENERO:":  # TODO: Permitir multiplas generos
                        index = palavras.index("GENERO:")
                        nova_lista = []
                        if index + 1 < len(palavras):
                            genero_busca = " ".join((palavras[index+1:]))
                            if "," in genero_busca:
                                genero_busca = genero_busca[0:genero_busca.index(
                                    ",")]
                            if "-" in genero_busca.split():
                                for palavraa in genero_busca.split():
                                    if palavraa != "-" and genero_busca.index("-")+1 < len(genero_busca) and palavraa not in nova_lista:
                                        nova_lista.append(palavraa)

                            if len(self.livros_filtrados) > 0:
                                livros_temp = []
                                if len(nova_lista) > 0:
                                    for p in nova_lista:
                                        for livro in self.livros_filtrados:
                                            if p in livro.get_genero():
                                                livros_temp.append(
                                                    livro)
                                else:
                                    for livro in self.livros_filtrados:
                                        if genero_busca in livro.get_genero():
                                            livros_temp.append(livro)
                                if len(livros_temp) > 0:
                                    self.livros_filtrados = livros_temp
                            else:
                                if len(nova_lista) > 0:
                                    for p in nova_lista:
                                        for livro in self.livros:
                                            if p in livro.get_genero():
                                                self.livros_filtrados.append(
                                                    livro)
                                else:
                                    for livro in self.livros:
                                        if genero_busca in livro.get_genero():
                                            self.livros_filtrados.append(livro)

                    case  "TITULO:":
                        index = palavras.index("TITULO:")
                        nova_lista = []

                        if index + 1 < len(palavras):
                            titulo_busca = " ".join((palavras[index+1:]))
                            if "," in titulo_busca:
                                titulo_busca = titulo_busca[0:titulo_busca.index(
                                    ",")]
                            if "-" in titulo_busca.split():
                                for palavraa in titulo_busca.split():
                                    if palavraa != "-" and titulo_busca.index("-")+1 < len(titulo_busca) and palavraa not in nova_lista:
                                        nova_lista.append(palavraa)
                            if len(self.livros_filtrados) > 0:
                                livros_temp = []
                                if len(nova_lista) > 0:
                                    for p in nova_lista:
                                        for livro in self.livros_filtrados:
                                            if p in livro.get_titulo():
                                                livros_temp.append(
                                                    livro)
                                else:
                                    for livro in self.livros_filtrados:
                                        if titulo_busca in livro.get_titulo():
                                            livros_temp.append(livro)
                                if len(livros_temp) > 0:
                                    self.livros_filtrados = livros_temp
                            else:
                                if len(nova_lista) > 0:
                                    for p in nova_lista:
                                        for livro in self.livros:
                                            if p in livro.get_titulo():
                                                self.livros_filtrados.append(
                                                    livro)

                                else:
                                    for livro in self.livros:
                                        if titulo_busca in livro.get_titulo():
                                            self.livros_filtrados.append(livro)

                    case  "QUANTIDADE:":
                        index = palavras.index("QUANTIDADE:")
                        nova_lista = []

                        if index + 1 < len(palavras):
                            try:
                                quantidade_busca = int(
                                    " ".join((palavras[index+1:])))
                                if "," in quantidade_busca:
                                    quantidade_busca = quantidade_busca[0:quantidade_busca.index(
                                        ",")]
                                if "-" in quantidade_busca.split():
                                    for palavraa in quantidade_busca.split():
                                        if palavraa != "-" and quantidade_busca.index("-")+1 < len(quantidade_busca) and palavraa not in nova_lista:
                                            nova_lista.append(palavraa)
                                quantidade_busca = int(quantidade_busca)
                                if len(self.livros_filtrados) > 0:
                                    livros_temp = []
                                    if len(nova_lista) > 0:
                                        for p in nova_lista:
                                            for livro in self.livros_filtrados:
                                                if p == livro.get_quant():
                                                    livros_temp.append(
                                                        livro)
                                    else:
                                        for livro in self.livros_filtrados:
                                            if quantidade_busca == livro.get_quant():
                                                livros_temp.append(livro)
                                    if len(livros_temp) > 0:
                                        self.livros_filtrados = livros_temp
                                else:
                                    if len(nova_lista) > 0:
                                        for p in nova_lista:
                                            for livro in self.livros:
                                                if p == livro.livro.get_quant():
                                                    self.livros_filtrados.append(
                                                        livro)

                                    else:
                                        for livro in self.livros:
                                            if quantidade_busca == livro.get_quant():
                                                self.livros_filtrados.append(
                                                    livro)
                            except ValueError:
                                self.notify("Valor inválido")

                    case  "AUTOR:":
                        index = palavras.index("AUTOR:")
                        nova_lista = []
                        if index + 1 < len(palavras):
                            autor_busca = " ".join((palavras[index+1:]))
                            if "," in autor_busca:
                                autor_busca = autor_busca[0:autor_busca.index(
                                    ",")]
                            if "-" in autor_busca.split():
                                for palavraa in autor_busca.split():
                                    if palavraa != "-" and autor_busca.index("-")+1 < len(autor_busca) and palavraa not in nova_lista:
                                        nova_lista.append(palavraa)
                            if len(self.livros_filtrados) > 0:
                                livros_temp = []
                                if len(nova_lista) > 0:
                                    for p in nova_lista:
                                        for livro in self.livros_filtrados:
                                            if p in livro.get_autor():
                                                livros_temp.append(
                                                    livro)
                                else:
                                    for livro in self.livros_filtrados:
                                        if autor_busca in livro.get_autor():
                                            livros_temp.append(livro)
                                if len(livros_temp) > 0:
                                    self.livros_filtrados = livros_temp
                            else:
                                if len(nova_lista) > 0:
                                    for p in nova_lista:
                                        for livro in self.livros:
                                            if p in livro.get_autor():
                                                self.livros_filtrados.append(
                                                    livro)

                                else:
                                    for livro in self.livros:
                                        if autor_busca in livro.get_autor():
                                            self.livros_filtrados.append(livro)

                    case "CODIGO:":
                        index = palavras.index("CODIGO:")
                        nova_lista = []

                        if index + 1 < len(palavras):
                            try:
                                codigo_busca = " ".join((palavras[index+1:]))
                                if "," in codigo_busca:
                                    codigo_busca = codigo_busca[0:codigo_busca.index(
                                        ",")]
                                if "-" in codigo_busca.split():
                                    for palavraa in codigo_busca.split():
                                        if palavraa != "-" and codigo_busca.index("-")+1 < len(codigo_busca) and palavraa not in nova_lista:
                                            nova_lista.append(palavraa)
                                codigo_busca = int(codigo_busca)
                                if len(self.livros_filtrados) > 0:
                                    livros_temp = []
                                    if len(nova_lista) > 0:
                                        for p in nova_lista:
                                            for livro in self.livros_filtrados:
                                                if p == livro.get_codigo():
                                                    livros_temp.append(
                                                        livro)
                                    else:
                                        for livro in self.livros_filtrados:
                                            if codigo_busca == livro.get_codigo():
                                                livros_temp.append(livro)
                                    if len(livros_temp) > 0:
                                        self.livros_filtrados = livros_temp
                                else:
                                    if len(nova_lista) > 0:
                                        for p in nova_lista:
                                            for livro in self.livros:
                                                if p == livro.get_codigo():
                                                    self.livros_filtrados.append(
                                                        livro)

                                    else:
                                        for livro in self.livros:
                                            if codigo_busca == livro.get_codigo():
                                                self.livros_filtrados.append(
                                                    livro)
                            except ValueError:
                                self.notify("Valor inválido")

                if len(self.livros_filtrados) > 0:
                    livros_str = [str(livro)
                                  for livro in self.livros_filtrados]
                    resultado.update(livros_str)
                    self.setup_dados()
                else:
                    livros_str = [str(livro) for livro in self.livros]
                    resultado.update(livros_str)
                    self.setup_dados()
        else:
            if len(self.livros_filtrados) > 0 and self.filtrou_select == False:
                livros_str = [str(livro)
                              for livro in self.livros_filtrados]
                resultado.update(livros_str)
                self.setup_dados()
            elif self.filtrou_select:
                self.select_changed(self.select_evento)
            else:
                livros_str = [str(livro) for livro in self.livros]
                resultado.update(livros_str)
                self.setup_dados()
