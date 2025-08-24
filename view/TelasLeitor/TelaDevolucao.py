from textual.widgets import Input, Pretty, TextArea, Button
from textual.containers import HorizontalGroup, Container
from controller import Controller
from model import Init


class TelaDevolucao(Container):

    CSS_PATH = "css/TelaDevolucao.tcss"

    def compose(self):
        with HorizontalGroup(id="hg_pesquisa"):
            yield Input()
            yield Button("Devolver", id="bt_devolver")
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        with HorizontalGroup(id="container"):
            pass

    emprestimos = Init.leitor1.get_lista_emprestimos()
    emprestimos_filtrados = []
    filtrou_checkbox = False
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    checkbox_evento = ""

    def setup_dados(self):
        if len(self.emprestimos_filtrados) > 0:
            quant = len(self.emprestimos_filtrados)
        else:
            quant = len(self.emprestimos)
        self.query_one(TextArea).text = f"Quantidade de Empréstimos: {quant}"

    def on_mount(self):
        emprestimos_str = [str(emprestimos)
                           for emprestimos in self.emprestimos]
        self.mount(Pretty(emprestimos_str))
        self.setup_dados()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_leitor")
            case "bt_devolver":
                cod_livro = self.query_one(Input).value
                devolucao = Controller.devolver(cod_livro, Init.leitor1.email)
                self.notify(devolucao)
                self.mount()

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        resultado = self.query_one(Pretty)
        palavras = texto.split()

        if len(palavras) > 0:
            if self.filtrou_select == False and self.filtrou_checkbox == False:
                self.emprestimos_filtrados = []

            for palavra in palavras:
                match palavra:

                    case "GENERO:":  # TODO: Permitir multiplas generos
                        index = palavras.index("GENERO:")
                        if index + 1 < len(palavras):
                            genero_busca = " ".join((palavras[index+1:]))
                            if "," in genero_busca:
                                genero_busca = genero_busca[0:genero_busca.index(
                                    ",")]
                            if len(self.emprestimos_filtrados) > 0:
                                emprestimos_temp = []
                                for emprestimo in self.emprestimos_filtrados:
                                    if emprestimo.get_livro().get_genero() == genero_busca:
                                        emprestimos_temp.append(emprestimo)
                                if len(emprestimos_temp) > 0:
                                    self.emprestimos_filtrados = emprestimos_temp
                            else:
                                for emprestimo in self.emprestimos:
                                    if emprestimo.get_livro().get_genero() == genero_busca:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)

                    case "TITULO:":
                        index = palavras.index("TITULO:")
                        if index + 1 < len(palavras):
                            titulo_busca = " ".join((palavras[index+1:]))
                            if "," in titulo_busca:
                                titulo_busca = titulo_busca[0:titulo_busca.index(
                                    ",")]
                            if len(self.emprestimos_filtrados) > 0:
                                emprestimos_temp = []
                                for emprestimo in self.emprestimos_filtrados:
                                    if emprestimo.get_livro().get_titulo() == titulo_busca:
                                        emprestimos_temp.append(emprestimo)
                                if len(emprestimos_temp) > 0:
                                    self.emprestimos_filtrados = emprestimos_temp
                            else:
                                for emprestimo in self.emprestimos:
                                    if emprestimo.get_livro().get_titulo() == titulo_busca:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)

                    case "QUANTIDADE:":
                        index = palavras.index("QUANTIDADE:")
                        if index + 1 < len(palavras):
                            try:
                                quantidade_busca = int(
                                    " ".join((palavras[index+1:])))
                                if "," in quantidade_busca:
                                    quantidade_busca = quantidade_busca[0:quantidade_busca.index(
                                        ",")]
                                quantidade_busca = int(quantidade_busca)
                                if len(self.emprestimos_filtrados) > 0:
                                    emprestimos_temp = []
                                    for emprestimo in self.emprestimos_filtrados:
                                        if emprestimo.get_livro().get_quant() == quantidade_busca:
                                            emprestimos_temp.append(emprestimo)
                                    if len(emprestimos_temp) > 0:
                                        self.emprestimos_filtrados = emprestimos_temp
                                else:
                                    for emprestimo in self.emprestimos:
                                        if emprestimo.get_livro().get_quant() == quantidade_busca:
                                            self.emprestimos_filtrados.append(
                                                emprestimo)
                            except ValueError:
                                self.notify("Valor inválido")

                    case "AUTOR:":
                        index = palavras.index("AUTOR:")
                        if index + 1 < len(palavras):
                            autor_busca = " ".join((palavras[index+1:]))
                            if "," in autor_busca:
                                autor_busca = autor_busca[0:autor_busca.index(
                                    ",")]
                            if len(self.emprestimos_filtrados) > 0:
                                emprestimos_temp = []
                                for emprestimo in self.emprestimos_filtrados:
                                    if emprestimo.get_livro().get_autor() == autor_busca:
                                        emprestimos_temp.append(emprestimo)
                                if len(emprestimos_temp) > 0:
                                    self.emprestimos_filtrados = emprestimos_temp
                            else:
                                for emprestimo in self.emprestimos:
                                    if emprestimo.get_livro().get_autor() == autor_busca:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)

                    case "CODIGO:":
                        index = palavras.index("CODIGO:")
                        if index + 1 < len(palavras):
                            try:
                                codigo_busca = " ".join((palavras[index+1:]))
                                if "," in codigo_busca:
                                    codigo_busca = codigo_busca[0:codigo_busca.index(
                                        ",")]
                                codigo_busca = int(codigo_busca)
                                if len(self.emprestimos_filtrados) > 0:
                                    emprestimos_temp = []
                                    for emprestimo in self.emprestimos_filtrados:
                                        if emprestimo.get_livro().get_codigo() == codigo_busca:
                                            emprestimos_temp.append(emprestimo)
                                    if len(emprestimos_temp) > 0:
                                        self.emprestimos_filtrados = emprestimos_temp
                                else:
                                    for emprestimo in self.emprestimos:
                                        if emprestimo.get_livro().get_codigo() == codigo_busca:
                                            self.emprestimos_filtrados.append(
                                                emprestimo)
                            except ValueError:
                                self.notify("Valor inválido")

                    case "NOME:":
                        index = palavras.index("NOME:")
                        if index + 1 < len(palavras):
                            nome_busca = " ".join((palavras[index+1:]))
                            if "," in nome_busca:
                                nome_busca = nome_busca[0:nome_busca.index(
                                    ",")]
                            if len(self.emprestimos_filtrados) > 0:
                                emprestimos_temp = []
                                for emprestimo in self.emprestimos_filtrados:
                                    if emprestimo.get_leitor().get_nome() == nome_busca:
                                        emprestimos_temp.append(emprestimo)
                                if len(emprestimos_temp) > 0:
                                    self.emprestimos_filtrados = emprestimos_temp
                            else:
                                for emprestimo in self.emprestimos:
                                    if emprestimo.get_leitor().get_nome() == nome_busca:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)

                    case "EMAIL:":
                        index = palavras.index("EMAIL:")
                        if index + 1 < len(palavras) and len(palavras[index + 1]) > 3:
                            email_busca = " ".join((palavras[index+1:]))
                            if "," in email_busca:
                                email_busca = email_busca[0:email_busca.index(
                                    ",")]
                            if len(self.emprestimos_filtrados) > 0:
                                emprestimos_temp = []
                                for emprestimo in self.emprestimos_filtrados:
                                    if emprestimo.get_leitor().get_email() == email_busca:
                                        emprestimos_temp.append(emprestimo)
                                if len(emprestimos_temp) > 0:
                                    self.emprestimos_filtrados = emprestimos_temp
                            else:
                                for emprestimo in self.emprestimos:
                                    if emprestimo.get_leitor().get_email() == email_busca:
                                        self.emprestimos_filtrados.append(
                                            emprestimo)

                if len(self.emprestimos_filtrados) > 0:
                    emprestimos_str = [str(emprestimo)
                                       for emprestimo in self.emprestimos_filtrados]
                    resultado.update(emprestimos_str)
                    self.setup_dados()
                else:
                    emprestimos_str = [str(emprestimo)
                                       for emprestimo in self.emprestimos]
                    resultado.update(emprestimos_str)
                    self.setup_dados()
        else:
            if len(self.emprestimos_filtrados) > 0 and self.filtrou_select == False:
                emprestimos_str = [str(emprestimo)
                                   for emprestimo in self.emprestimos_filtrados]
                resultado.update(emprestimos_str)
                self.setup_dados()
            elif self.filtrou_select:
                self.select_changed(self.select_evento)
            else:
                emprestimos_str = [str(emprestimo)
                                   for emprestimo in self.emprestimos]
                resultado.update(emprestimos_str)
                self.setup_dados()
