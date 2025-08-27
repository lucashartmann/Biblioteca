from textual.widgets import Input, Pretty, TextArea, Button
from textual.containers import HorizontalGroup, Container
from textual.containers import HorizontalGroup
from controller import Controller


class TelaClientela(Container):

    def compose(Container):
        with HorizontalGroup(id="hg_pesquisa"):
            yield Input()
            yield Button("Remover", id="bt_remover")
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(read_only=True)
        with HorizontalGroup(id="container"):
            pass

    leitores = Controller.get_leitores_biblioteca()
    leitores_filtrados = []
    montou = False

    def setup_dados(self):
        if len(self.leitores_filtrados) > 0:
            quant = len(self.leitores_filtrados)
        else:
            quant = len(self.leitores)
        self.query_one(TextArea).text = f"Quantidade de leitores: {quant}"

    def on_mount(self):
        leitores_str = [str(leitor) for leitor in self.leitores]
        if self.montou:
            self.query_one(Pretty).update(leitores_str)
        else:
            self.mount(Pretty(leitores_str))
            self.montou = True

        self.setup_dados()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_remover":
                input_email = self.query_one(Input).value
                mensagem = Controller.excluir_leitor(input_email.upper())
                self.notify(str(mensagem), markup=False)
                self.atualizar()

    def atualizar(self):
        resultado = self.query_one(Pretty)
        if len(self.leitores_filtrados) > 0:
            leitores_str = [str(leitor)
                            for leitor in self.leitores_filtrados]
            resultado.update(leitores_str)
            self.setup_dados()
        else:
            leitores_str = [str(leitor) for leitor in self.leitores]
            resultado.update(leitores_str)
            self.setup_dados()

    def filtro(self, palavras, index, filtro):
        campo = f"get_{filtro}"
        nova_lista = []
        if index + 1 < len(palavras):
            nome_busca = " ".join((palavras[index+1:]))
            if "," in nome_busca:
                nome_busca = nome_busca[0:nome_busca.index(
                    ",")]
            if "-" in nome_busca.split():
                for palavraa in nome_busca.split("-"):
                    if nome_busca.index("-")+1 < len(nome_busca) and palavraa not in nova_lista:
                        nova_lista.append(palavraa.split())
            if len(self.leitores_filtrados) > 0:
                leitores_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for leitor in self.leitores_filtrados:
                            if p in getattr(leitor, campo)() and leitor not in leitores_temp:
                                leitores_temp.append(
                                    leitor)
                else:
                    for leitor in self.leitores_filtrados:
                        if nome_busca in getattr(leitor, campo)() and leitor not in leitores_temp:
                            leitores_temp.append(leitor)
                if len(leitores_temp) > 0:
                    self.leitores_filtrados = leitores_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for leitor in self.leitores:
                            if p in getattr(leitor, campo)() and leitor not in self.leitores_filtrados:
                                self.leitores_filtrados.append(
                                    leitor)
                else:
                    for leitor in self.leitores:
                        if nome_busca in getattr(leitor, campo)() and leitor not in self.leitores_filtrados:
                            self.leitores_filtrados.append(
                                leitor)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        palavras = texto.split()

        if len(palavras) > 0:
            self.leitores_filtrados = []

            for palavra in palavras:
                match palavra:
                    case "NOME:":
                        index = palavras.index("NOME:")
                        self.filtro(palavras, index, "nome")

                    case "EMAIL:":
                        index = palavras.index("EMAIL:")
                        self.filtro(palavras, index, "email")

                self.atualizar()
        else:
            self.atualizar()
