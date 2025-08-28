from textual.widgets import Label, Button, ListItem, ListView, Footer, Header, Static, Select, Input
from controller import Controller
from textual import on
from textual.screen import Screen
from textual.containers import VerticalScroll, HorizontalGroup
from textual.binding import Binding
from model import Init
from textual.message import Message


class RetiradaRealizada(Message):
    def __init__(self, sender) -> None:
        super().__init__()
        self.sender = sender

# assets/c4.jpg 

class TelaEstoqueCapas(Screen):

    CSS_PATH = "css/TelaEstoqueCapas.tcss"

    BINDINGS = [
        Binding("ctrl+l", "app.switch_screen('tela_inicial')", "Voltar")
    ]

    livros = Init.biblioteca.get_lista_livros()
    livros_filtrados = []

    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    montou = False

    def atualizar_capas(self):
        list_view = self.query_one("#lst_item", ListView)
        list_view.clear()
        # contador = 0
        lista = self.livros
        if len(self.livros_filtrados) > 0:
            lista = self.livros_filtrados

        for i, livro in enumerate(lista):
            self.notify(livro.get_caminho_capa())
            if livro.get_capa_pixel():
                # contador += 1

                static = Static(livro.get_capa())
                static.styles.width = livro.get_largura_capa()
                static.styles.height = livro.get_altura_capa()

                list_item = ListItem(static)
                list_item.styles.width = livro.get_largura_capa() - 10
                list_item.styles.height = livro.get_altura_capa() - 15

                list_view.append(list_item)

                # if contador == 3:
                #     prateleira_pixels = Controller.gerar_pixel("assets/prat.png", 60, 200)
                #     if prateleira_pixels:
                #         prateleira_static = Static(prateleira_pixels, id=f"prateleira{i}")
                #         prateleira_item = ListItem(prateleira_static, id=f"prateleira_item{i}")
                #         list_view.append(prateleira_item)
                #     contador = 0

    def _on_screen_resume(self):
        self.livros = Init.biblioteca.get_lista_livros()
        
        if Init.usuario_leitor:
            lista_usuario = []
            for livro in self.livros:
                if livro.is_disponivel():
                    lista_usuario.append(livro)
            self.livros = lista_usuario
            
            
        lista_categorias = []
        for livro in self.livros:
            if livro.get_genero() not in lista_categorias:
                lista_categorias.append(livro.get_genero())
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])
        self.atualizar_capas()

    def compose(self):
        yield Header()
        with VerticalScroll():
            with HorizontalGroup(id="hg_pesquisa"):
                yield Select([("genero", 'genero')])
                yield Input()
                if Init.usuario_leitor:
                    yield Button("Retirar", id="bt_retirar")
                else:
                    yield Button("Remover", id="bt_remover")
                yield Button("Voltar", id="bt_voltar")
            yield ListView(id="lst_item")
            yield Label("item", id="tx_info")

            yield Footer()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_retirar":
                cod_livro = self.query_one(Input).value
                retirada = Controller.emprestar(
                    cod_livro, Init.leitor1.get_email())
                self.notify(retirada)
                self.atualizar_capas()
                self.post_message(RetiradaRealizada(self))
            case "bt_remover":
                input_id = self.query_one(Input).value
                mensagem = Controller.excluir_livro(input_id)
                self.notify(str(mensagem), markup=False)
                self.post_message(RetiradaRealizada(self))
                self.atualizar_capas()

    @on(ListView.Highlighted, "#lst_item")
    def item_selecionado(self) -> None:
        lista = self.query_one("#lst_item", ListView)
        info = self.query_one("#tx_info", Label)
        try:
            nome_item = self.livros[lista.index + 1].get_titulo()
            info.update(f"{nome_item}")
        except:
            pass

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        if evento.select.is_blank():
            if self.filtrou_input == False and self.filtrou_select:
                self.livros_filtrados = []
            self.filtrou_select = False
            self.atualizar_capas()
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

            self.filtrou_select = True
            self.select_evento = evento
            self.atualizar_capas()

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

                    case  "TITULO:":
                        index = palavras.index("TITULO:")
                        self.filtro(palavras, index, "titulo")

                    case  "QUANTIDADE:":
                        index = palavras.index("QUANTIDADE:")
                        self.filtro(palavras, index, "quant")

                    case  "AUTOR:":
                        index = palavras.index("AUTOR:")
                        self.filtro(palavras, index, "autor")

                    case "CODIGO:":
                        index = palavras.index("CODIGO:")
                        self.filtro(palavras, index, "codigo")

                self.atualizar_capas()
        else:
            if len(self.livros_filtrados) > 0 and self.filtrou_select == False:
                self.atualizar_capas()
            elif self.filtrou_select:
                self.select_changed(self.select_evento)
            else:
                self.atualizar_capas()
