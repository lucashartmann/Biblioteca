class Livro:

    def __init__(self, titulo, autor, genero, quant):
        self.codigo = 0
        self.capa = ""
        self.caminho_capa = ""
        self.largura_capa = 0
        self.altura_capa = 0
        self.autor = autor
        self.genero = genero
        self.titulo = titulo
        self.quant = quant
        self.disponivel = True
        
    def set_codigo(self, novo_codigo):
        self.codigo = novo_codigo
        
    def get_codigo(self):
        return self.codigo

    def get_largura_capa(self):
        return self.largura_capa

    def get_altura_capa(self):
        return self.altura_capa

    def set_largura_capa(self, novo_largura_capa):
        self.largura_capa = novo_largura_capa

    def set_altura_capa(self, novo_altura_capa):
        self.altura_capa = novo_altura_capa

    def set_caminho_capa(self, novo_caminho):
        self.caminho_capa = novo_caminho
        
    def get_caminho_capa(self):
        return self.caminho_capa
    
    def set_disponivel(self, novo_disponivel):
        self.disponivel = novo_disponivel

    def get_capa(self):
        return self.capa

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
        return f"Livro [Titulo = {self.get_titulo()}, Autor = {self.get_autor()}, Genero = {self.get_genero()}, Quantidade = {self.get_quant()}, Disponivel = {self.is_disponivel()}]"
