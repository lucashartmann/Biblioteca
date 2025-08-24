from textual.widgets import Label, ListItem, ListView, Footer, Header,  Static
from controller import Controller
from textual import on
from textual.screen import Screen


class TelaEstoqueCapas(Screen):

    CSS_PATH = "css/TelaEstoqueCapas.tcss"

    mapa_livros = Controller.get_livros_biblioteca()

    def on_mount(self):
        list_view = self.query_one("#lst_item", ListView)
        list_view.clear()
        for livro in self.mapa_livros.values():
            if livro.get_capa():
                list_view.append(
                    ListItem(Static(livro.capa)))

    def compose(self):
        yield Header()
        yield ListView(id="lst_item")
        yield Label("item", id="tx_info")
        yield Footer()

    @on(ListView.Highlighted, "#lst_item")
    def item_selecionado(self) -> None:
        lista = self.query_one("#lst_item", ListView)
        info = self.query_one("#tx_info", Label)
        nome_item = self.lista_items[lista.index].titulo
        if nome_item in self.descricoes.keys():
            info.update(f"{self.descricoes[nome_item].get_titulo()}")
