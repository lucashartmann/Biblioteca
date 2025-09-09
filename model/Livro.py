
class Livro:

    def __init__(self, titulo, autor, genero, quant):
        self.codigo = 0
        self.capa_binaria = ""
        self.autor = autor
        self.genero = genero
        self.titulo = titulo
        self.quant = quant
        self.disponivel = True

    def set_capa_binaria(self, caminho):
        if type(caminho) == str:
            if "." in caminho or "/" in caminho or "//" in caminho:
                with open(caminho, 'rb') as f:
                    binario_imagem = f.read()
                self.capa_binaria = binario_imagem
        else:
            self.capa_binaria = caminho

    def set_codigo(self, novo_codigo):
        self.codigo = novo_codigo

    def get_codigo(self):
        return self.codigo

    def set_disponivel(self, novo_disponivel):
        self.disponivel = novo_disponivel

    def get_capa_binaria(self):
        return self.capa_binaria

    def get_autor(self):
        return self.autor

    def get_genero(self):
        return self.genero

    def get_titulo(self):
        return self.titulo

    def get_quant(self):
        return self.quant

    def is_disponivel(self):
        return self.disponivel

    def set_autor(self, novo_autor):
        self.autor = novo_autor

    def set_genero(self, novo_genero):
        self.genero = novo_genero

    def set_titulo(self, novo_titulo):
        self.titulo = novo_titulo

    def set_capa(self, nova_capa):
        self.capa = nova_capa

    def set_quant(self, novo_quant):
        self.quant = novo_quant

    def atualizar_disponivel(self):
        if self.get_quant() == 0:
            self.disponivel = False
        else:
            self.disponivel = True

    def __str__(self):
        return f"Livro [Código = {self.get_codigo()}, Titulo = {self.get_titulo()}, Autor = {self.get_autor()}, Genero = {self.get_genero()}, Quantidade = {self.get_quant()}, Disponivel = {self.is_disponivel()}]"
