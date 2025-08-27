import sys
from model import Leitor, Livro, Init, Banco
from rich_pixels import Pixels
from PIL import Image
import os


def get_capa(cod_livro):
    try:
        cod_livro = int(cod_livro)
    except:
        return f"ERRO ao converter {cod_livro}"

    livro = Init.biblioteca.get_livro_por_cod(cod_livro)
    if livro.get_capa():
        return livro.get_capa()
    else:
        return None


def resize(caminho, largura, altura):
    size = largura, altura

    if not os.path.exists(caminho):
        print(f"Imagem não encontrada: {caminho}")
        return False, ""

    try:
        im = Image.open(caminho)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        novo_caminho = f"{caminho.split('.')[0]}copia.{caminho.split('.')[1]}"
        if os.path.exists(novo_caminho):
            os.remove(novo_caminho)
        im.save(novo_caminho)
    except ValueError:
        print(caminho)
        print(novo_caminho)
        return False, ""
    return True, novo_caminho


def gerar_pixel(caminho, largura, altura):
    if largura and altura:
        bool, novo_caminho = resize(caminho, largura, altura)
    else:
        im = Image.open(caminho)
        novo_caminho = f"{caminho.split('.')[0]}copia.{caminho.split('.')[1]}"
        if os.path.exists(novo_caminho):
            os.remove(novo_caminho)
        im.save(novo_caminho)
        bool = True
    if bool:
        try:
            pixels = Pixels.from_image_path(novo_caminho)
            if os.path.exists(novo_caminho):
                os.remove(novo_caminho)
            return pixels
        except Exception:
            print(f"Erro ao gerar pixels")
            return None
    return None

def salvar_no_banco():
    Init.banco_dados.criar_tabela("Leitor")
    for leitor in Init.biblioteca.get_lista_leitores().values():
            dados = [(leitor.get_nome(), leitor.get_email())]
            if not Init.banco_dados.consulta_dado("Leitor", leitor.get_email()):
                Init.banco_dados.inserir_dados(dados, "Leitor")
    return "Leitores salvos com sucesso"

def is_pyinstaller():
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return True, base_path
    else:
        return False, ""


if not Init.carregar_biblioteca:
    e_exe, caminho = is_pyinstaller()
    print(caminho)
    print(f"{caminho}\\assets\\c0.jpg")

    if e_exe:
        Init.livro1.set_capa(gerar_pixel(f"{caminho}\\assets\\c0.jpg", 30, 30))
        Init.livro2.set_capa(gerar_pixel(f"{caminho}\\assets\\c1.jpg", 30, 30))
        Init.livro3.set_capa(gerar_pixel(f"{caminho}\\assets\\c2.jpg", 30, 30))
        Init.livro4.set_capa(gerar_pixel(f"{caminho}\\assets\\c3.jpg", 30, 30))
    else:
        Init.livro1.set_capa(gerar_pixel("assets\\c0.jpg", 30, 30))
        Init.livro2.set_capa(gerar_pixel("assets\\c1.jpg", 30, 30))
        Init.livro3.set_capa(gerar_pixel("assets\\c2.jpg", 30, 30))
        Init.livro4.set_capa(gerar_pixel("assets\\c3.jpg", 30, 30))

    Init.livro1.set_largura_capa(30)
    Init.livro2.set_largura_capa(30)
    Init.livro3.set_largura_capa(30)
    Init.livro4.set_largura_capa(30)

    Init.livro1.set_altura_capa(30)
    Init.livro2.set_altura_capa(30)
    Init.livro3.set_altura_capa(30)
    Init.livro4.set_altura_capa(30)
else:
    livro1 = Init.biblioteca.get_livro_por_cod(1)
    livro2 = Init.biblioteca.get_livro_por_cod(2)
    livro3 = Init.biblioteca.get_livro_por_cod(3)
    livro4 = Init.biblioteca.get_livro_por_cod(4)

    livro1.set_largura_capa(30)
    livro2.set_largura_capa(30)
    livro3.set_largura_capa(30)
    livro4.set_largura_capa(30)

    livro1.set_altura_capa(30)
    livro2.set_altura_capa(30)
    livro3.set_altura_capa(30)
    livro4.set_altura_capa(30)


def get_livros_biblioteca():
    return Init.biblioteca.get_lista_livros()


def get_leitores_biblioteca():
    return Init.biblioteca.get_lista_leitores()


def emprestar(cod_livro, email):
    if cod_livro == "":
        return "ERRO. Código do livro está vazio"

    if email == "":
        return "ERRO. Email do leitor está vazio"

    try:
        cod_livro = int(cod_livro)
    except:
        return f"ERRO ao converter {cod_livro}"

    livro = Init.biblioteca.get_livro_por_cod(cod_livro)
    leitor = Init.biblioteca.get_leitor_por_email(email)

    if not livro:
        return f"Erro, livro '{cod_livro}' não existe"

    if not leitor:
        return f"Erro, leitor '{email}' não existe"

    emprestimo = Init.biblioteca.emprestar(livro, leitor)

    if emprestimo:
        adicao = leitor.add_emprestimo(emprestimo)
        if adicao:
            return f"Livro '{livro.get_titulo()}' emprestado com sucesso"
        else:
            "Erro ao adicionar emprestimo ao leitor"
    else:
        return f"Erro ao emprestar livro '{livro.get_titulo()}', livro não está disponivel"


def devolver(id_emprestimo, email):
    if id_emprestimo == "":
        return "ERRO. ID do Empréstimo está vazio"
    try:
        id_emprestimo = int(id_emprestimo)
    except:
        return f"ERRO ao converter {id_emprestimo}"

    leitor = Init.biblioteca.get_leitor_por_email(email)

    if not leitor:
        return f"Erro, leitor '{email}' não existe"

    emprestimo = leitor.get_emprestimo_por_id(id_emprestimo)
    livro = emprestimo.get_livro()

    if not emprestimo:
        return f"Erro, empréstimo com id '{id_emprestimo}' não existe"

    devolucao = Init.biblioteca.devolver(emprestimo)

    if devolucao:
        return f"Livro '{livro.get_titulo()}' devolvido com sucesso"
    else:
        return f"Erro ao devolver livro '{livro.get_titulo()}' do empréstimo '{id_emprestimo}'"


def cadastrar_livro(dados):
    titulo = dados[0]
    autor = dados[1]
    quant = dados[2]
    caminho_capa = dados[3]
    largura_capa = dados[4]
    altura_capa = dados[5]
    genero = dados[-1]

    if titulo == "":
        return "Erro, titulo vazio"

    if autor == "":
        return "Erro, autor vazio"

    if genero == "":
        return "Erro, genero vazio"

    if quant == "":
        return "Erro, quant vazio"

    try:
        quant = int(quant)
    except:
        return f"Erro ao converter '{quant}'"

    livro = Livro.Livro(titulo, autor, genero, quant)

    if caminho_capa != "" and largura_capa != "" and altura_capa != "":
        try:
            altura_capa = int(altura_capa)
            largura_capa = int(largura_capa)
            gerar_capa = gerar_pixel(caminho_capa, largura_capa, altura_capa)
            if gerar_capa:
                livro.set_capa(gerar_capa)
                livro.set_largura_capa(largura_capa)
                livro.set_altura_capa(altura_capa)
            else:
                return "Erro ao gerar capa"
        except:
            return f"Erro ao converter '{altura_capa}' e '{largura_capa}'"

    if caminho_capa != "" and largura_capa == "" and altura_capa == "":
        if livro.get_altura_capa() and livro.get_largura_capa():
            gerar_capa = gerar_pixel(
                caminho_capa, livro.get_largura_capa(), livro.get_altura_capa())
        else:
            gerar_capa = gerar_pixel(caminho_capa, largura_capa, altura_capa)
        if gerar_capa:
            livro.set_capa(gerar_capa)
        else:
            return "Erro ao gerar capa"

    if caminho_capa == "" and largura_capa != "" and altura_capa != "":
        try:
            largura_capa = int(largura_capa)
            altura_capa = int(altura_capa)
            if livro.get_caminho_capa():
                gerar_capa = gerar_pixel(
                    livro.get_caminho_capa(), largura_capa, altura_capa)
                if gerar_capa:
                    livro.set_capa(gerar_capa)
                    livro.set_largura_capa(largura_capa)
                    livro.set_altura_capa(altura_capa)
                else:
                    return "Erro ao gerar capa"
            else:
                return "Capa precisa ter um caminho"
        except:
            return f"Erro ao converter '{largura_capa}' e '{altura_capa}'"

    if caminho_capa == "" and largura_capa != "" and altura_capa == "":
        return "Altura não pode estar vazia"

    if caminho_capa == "" and largura_capa == "" and altura_capa != "":
        return "Largura não pode estar vazia"

    if not livro:
        return "ERRO ao criar livro"

    cadastro = Init.biblioteca.add_livro(livro)

    if cadastro:
        return f"Livro cadastrado com sucesso\n{livro}"
    return "ERRO ao cadastrar livro"


def cadastrar_leitor(dados):
    nome = dados[0]
    email = dados[1]

    if nome == "":
        return "Erro, nome vazio"

    if email == "":
        return "Erro, email vazio"

    leitor = Leitor.Leitor(nome, email)

    if not leitor:
        return "ERRO ao criar leitor"

    cadastro = Init.biblioteca.add_leitor(leitor)

    if cadastro:
        Init.leitor1 = leitor
        return f"Leitor cadastrado com sucesso\n{leitor}"
    return "ERRO ao cadastrar leitor"


def excluir_leitor(email):

    if email == "":
        return "ERRO. Email do leitor está vazio"

    remocao = Init.biblioteca.remove_leitor(email)

    if remocao:
        return f"Leitor '{email}' removido com sucesso"
    else:
        return f"Erro, leitor '{email}' não existe"


def excluir_livro(cod_livro):
    if cod_livro == "":
        return "ERRO. Código do livro está vazio"

    try:
        cod_livro = int(cod_livro)
    except:
        return f"ERRO ao converter '{cod_livro}'"

    remocao = Init.biblioteca.remove_livro(cod_livro)

    if remocao:
        return f"Livro '{cod_livro}' removido com sucesso!"
    else:
        return f"Erro, não existe livro com código '{cod_livro}'"


def editar_leitor(email, dados):

    if email == "":
        return "ERRO. Email do leitor está vazio"

    leitor = Init.biblioteca.get_leitor_por_email(email)

    if not leitor:
        return f"Erro, leitor '{email}' não existe"

    mensagem = ""

    novo_nome = dados[0]
    novo_email = dados[1]

    if novo_nome != "":
        leitor.set_nome(novo_nome)
        mensagem += f"Nome editado '{novo_nome}'\n"
    if novo_email != "":
        if Init.biblioteca.get_leitor_por_email(novo_email):
            mensagem += f"Erro, '{novo_email}' já cadastrado"
        else:
            Init.biblioteca.remove_leitor(email)
            leitor.set_email(novo_email)
            Init.biblioteca.add_leitor(leitor)
            mensagem += f"Email editado '{novo_email}'"
    return mensagem


def editar_livro(cod_livro, dados):
    if cod_livro == "":
        return "ERRO. Código do livro está vazio"

    try:
        cod_livro = int(cod_livro)
    except:
        return f"ERRO ao converter '{cod_livro}'"

    livro = Init.biblioteca.get_livro_por_cod(cod_livro)

    if not livro:
        return f"Erro, não existe livro com código '{cod_livro}'"

    mensagem = ""

    titulo = dados[0]
    autor = dados[1]
    quant = dados[2]
    caminho_capa = dados[3]
    largura_capa = dados[4]
    altura_capa = dados[5]
    genero = dados[-1]

    if titulo != "":
        livro.set_titulo(titulo)
        mensagem += f"Titulo editado '{titulo}'\n"
    if autor != "":
        livro.set_autor(autor)
        mensagem += f"Autor editado '{autor}'\n"
    if genero != "":
        livro.set_genero(genero)
        mensagem += f"Genero editado '{genero}'\n"
    if quant != "":
        try:
            quant = int(quant)
            livro.set_quant(quant)
            mensagem += f"Quant editado '{quant}'"
        except:
            mensagem += f"Erro ao converter '{quant}'"

    if caminho_capa != "" and largura_capa != "" and altura_capa != "":
        try:
            altura_capa = int(altura_capa)
            largura_capa = int(largura_capa)
            gerar_capa = gerar_pixel(caminho_capa, largura_capa, altura_capa)
            if gerar_capa:
                livro.set_capa(gerar_capa)
                livro.set_largura_capa(largura_capa)
                livro.set_altura_capa(altura_capa)
                mensagem += f"Capa editada\n"
            else:
                mensagem += "Erro ao gerar capa"
        except:
            mensagem += f"Erro ao converter '{altura_capa}' e '{largura_capa}'"

    if caminho_capa != "" and largura_capa == "" and altura_capa == "":
        if livro.get_altura_capa() and livro.get_largura_capa():
            gerar_capa = gerar_pixel(
                caminho_capa, livro.get_largura_capa(), livro.get_altura_capa())
        else:
            gerar_capa = gerar_pixel(caminho_capa, largura_capa, altura_capa)
        if gerar_capa:
            livro.set_capa(gerar_capa)
            mensagem += f"Caminho editado\n"
        else:
            mensagem += "Erro ao gerar capa"

    if caminho_capa == "" and largura_capa != "" and altura_capa != "":
        try:
            largura_capa = int(largura_capa)
            altura_capa = int(altura_capa)
            if livro.get_caminho_capa():
                gerar_capa = gerar_pixel(
                    livro.get_caminho_capa(), largura_capa, altura_capa)
                if gerar_capa:
                    livro.set_capa(gerar_capa)
                    livro.set_largura_capa(largura_capa)
                    livro.set_altura_capa(altura_capa)
                    mensagem += f"Tamanho editado\n"
                else:
                    mensagem += "Erro ao gerar capa"
            else:
                mensagem += "Capa precisa ter um caminho"
        except:
            mensagem += f"Erro ao converter '{largura_capa}' e '{altura_capa}'"

    if caminho_capa == "" and largura_capa != "" and altura_capa == "":
        mensagem += "Altura não pode estar vazia"

    if caminho_capa == "" and largura_capa == "" and altura_capa != "":
        mensagem += "Largura não pode estar vazia"

    return mensagem
