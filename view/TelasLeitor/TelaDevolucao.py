from textual.widgets import Input, Pretty, TextArea, Button
from textual.containers import HorizontalGroup, VerticalScroll
from controller import Controller
from model import Init, Livro, Leitor
from textual.message import Message


class DevolucaoRealizada(Message):
    def __init__(self, sender) -> None:
        super().__init__()
        self.sender = sender


class TelaDevolucao(VerticalScroll):

    def compose(self):
        with HorizontalGroup(id="hg_pesquisa"):
            yield Input(placeholder="ID do empréstimo aqui")
            yield Button("Devolver", id="bt_devolver")
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(read_only=True)
        with HorizontalGroup(id="container"):
            pass

    emprestimos = Init.leitor1.get_lista_emprestimos()
    emprestimos_filtrados = []
    filtrou_checkbox = False
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    checkbox_evento = ""
    montou = False

    def setup_dados(self):
        if len(self.emprestimos_filtrados) > 0:
            quant = len(self.emprestimos_filtrados)
        else:
            quant = len(self.emprestimos)
        self.query_one(
            TextArea).text = f"Exemplo de busca: 'titulo: Maus - 1984, nome: lucas' \n\nQuantidade de Empréstimos: {quant}"

    def on_mount(self):
        self.emprestimos = Init.leitor1.get_lista_emprestimos()
        emprestimos_str = []
        if self.montou:
            self.query_one(Pretty).update(emprestimos_str)
        else:
            self.mount(Pretty(emprestimos_str))
            self.montou = True
        self.atualizar()
        self.setup_dados()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_devolver":
                cod_livro = self.query_one(Input).value
                devolucao = Controller.devolver(cod_livro, Init.leitor1.email)
                self.notify(devolucao)
                self.on_mount()
                self.post_message(DevolucaoRealizada(self))

    def atualizar(self):
        resultado = self.query_one(Pretty)
        emprestimos_str = []
        lista = self.emprestimos
        if len(self.emprestimos_filtrados) > 0:
            lista = self.emprestimos_filtrados
        for emprestimo in lista:
            emprestimo_str = str(emprestimo).split(",")[:-1]
            emprestimos_str.append(emprestimo_str)
        resultado.update(emprestimos_str)
        self.setup_dados()

    def filtro(self, palavras, index, filtro_recebido):
        lista_filtros = ["quant", "codigo"]
        lista_filtros_leitor = ["nome", "email"]
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
                    filtro = filtro.strip()
                    filtro = int(filtro)
                except ValueError:
                    self.notify("Valor Inválido")
                    return

            if len(self.emprestimos_filtrados) > 0:
                emprestimos_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for emprestimo in self.emprestimos_filtrados:
                            if filtro_recebido in lista_filtros_leitor:
                                if type(filtro) == int:
                                    if p == getattr(emprestimo.get_leitor(), campo)() and emprestimo not in emprestimos_temp:
                                        emprestimos_temp.append(
                                            emprestimo)
                                else:
                                    if p in getattr(emprestimo.get_leitor(), campo)() and emprestimo not in emprestimos_temp:
                                        emprestimos_temp.append(
                                            emprestimo)
                            else:
                                if type(filtro) == int:
                                    if p == getattr(emprestimo.get_livro(), campo)() and emprestimo not in emprestimos_temp:
                                        emprestimos_temp.append(
                                            emprestimo)
                                else:
                                    if p in getattr(emprestimo.get_livro(), campo)() and emprestimo not in emprestimos_temp:
                                        emprestimos_temp.append(
                                            emprestimo)
                else:
                    for emprestimo in self.emprestimos_filtrados:
                        if filtro_recebido in lista_filtros_leitor:
                            if type(filtro) == int:
                                if p in getattr(emprestimo.get_leitor(), campo)() and emprestimo not in emprestimos_temp:
                                    emprestimos_temp.append(
                                        emprestimo)
                            else:
                                if p in getattr(emprestimo.get_leitor(), campo)() and emprestimo not in emprestimos_temp:
                                    emprestimos_temp.append(
                                        emprestimo)
                        else:
                            if type(filtro) == int:
                                if filtro == getattr(emprestimo.get_livro(), campo)() and emprestimo not in emprestimos_temp:
                                    emprestimos_temp.append(emprestimo)
                            else:
                                if filtro in getattr(emprestimo.get_livro(), campo)() and emprestimo not in emprestimos_temp:
                                    emprestimos_temp.append(emprestimo)
                if len(emprestimos_temp) > 0:
                    self.emprestimos_filtrados = emprestimos_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for emprestimo in self.emprestimos:
                            if filtro_recebido in lista_filtros_leitor:
                                if type(filtro) == int:
                                    if p == getattr(emprestimo.get_leitor(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)
                                else:
                                    if p in getattr(emprestimo.get_leitor(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)
                            else:
                                if type(filtro) == int:
                                    if p == getattr(emprestimo.get_livro(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)
                                else:
                                    if p in getattr(emprestimo.get_livro(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)
                else:
                    for emprestimo in self.emprestimos:
                        if filtro_recebido in lista_filtros_leitor:
                            if type(filtro) == int:
                                if filtro == getattr(emprestimo.get_leitor(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                    self.emprestimos_filtrados.append(
                                        emprestimo)
                            else:
                                if filtro in getattr(emprestimo.get_leitor(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                    self.emprestimos_filtrados.append(
                                        emprestimo)
                        else:
                            if type(filtro) == int:
                                if filtro == getattr(emprestimo.get_livro(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                    self.emprestimos_filtrados.append(
                                        emprestimo)
                            else:
                                if filtro in getattr(emprestimo.get_livro(), campo)() and emprestimo not in self.emprestimos_filtrados:
                                    self.emprestimos_filtrados.append(
                                        emprestimo)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        palavras = texto.split()

        if len(palavras) > 0:
            if self.filtrou_select == False and self.filtrou_checkbox == False:
                self.emprestimos_filtrados = []

            for palavra in palavras:
                match palavra:

                    case "GENERO:":
                        index = palavras.index("GENERO:")

                    case "TITULO:":
                        index = palavras.index("TITULO:")
                        self.filtro(palavras, index, "titulo")

                    case "QUANTIDADE:":
                        index = palavras.index("QUANTIDADE:")
                        self.filtro(palavras, index, "quant")

                    case "AUTOR:":
                        index = palavras.index("AUTOR:")
                        self.filtro(palavras, index, "autor")

                    case "CODIGO:":
                        index = palavras.index("CODIGO:")
                        self.filtro(palavras, index, "codigo")

                    case "NOME:":
                        index = palavras.index("NOME:")
                        self.filtro(palavras, index, "nome")

                    case "EMAIL:":
                        index = palavras.index("EMAIL:")
                        self.filtro(palavras, index, "email")

                self.atualizar()
        else:
            if self.filtrou_select == False:
                self.atualizar()
            elif self.filtrou_select:
                self.select_changed(self.select_evento)
            else:
                self.atualizar()
