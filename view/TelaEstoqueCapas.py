from textual.widgets import Label, ListItem, ListView, Footer, Header,  Static
from controller import Controller
from textual import on
from textual.screen import Screen
from textual.containers import VerticalScroll
from textual.binding import Binding

class TelaEstoqueCapas(Screen):

    CSS_PATH = "css/TelaEstoqueCapas.tcss"

    BINDINGS = [
        Binding("x", "app.switch_screen('tela_inicial')", "Voltar")
    ]


    mapa_livros = Controller.get_livros_biblioteca()


    def _on_screen_resume(self):
        list_view = self.query_one("#lst_item", ListView)
        list_view.clear()
        # contador = 0
        for i, livro in enumerate(self.mapa_livros.values()):
            if livro.get_capa():
                # contador += 1

                static = Static(livro.get_capa())
                static.styles.width = livro.get_largura_capa()
                static.styles.height = livro.get_altura_capa()

                list_item = ListItem(static)
                list_item.styles.width = livro.get_largura_capa() - 10
                list_item.styles.height = livro.get_altura_capa()

                list_view.append(list_item)

                # if contador == 3:
                #     prateleira_pixels = Controller.gerar_pixel("assets/prat.png", 60, 200)
                #     if prateleira_pixels:
                #         prateleira_static = Static(prateleira_pixels, id=f"prateleira{i}")
                #         prateleira_item = ListItem(prateleira_static, id=f"prateleira_item{i}")
                #         list_view.append(prateleira_item)
                #     contador = 0

    def compose(self):
        yield Header()
        with VerticalScroll():
            yield ListView(id="lst_item")
            yield Label("item", id="tx_info")
            yield Footer()

    @on(ListView.Highlighted, "#lst_item")
    def item_selecionado(self) -> None:
        lista = self.query_one("#lst_item", ListView)
        info = self.query_one("#tx_info", Label)

        nome_item = self.mapa_livros[lista.index+1].get_titulo()
        info.update(f"{nome_item}")
