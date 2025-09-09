import sys
from model import Leitor, Livro, Init
from rich_pixels import Pixels
from PIL import Image
import os


def fechar_banco():
    if Init.biblioteca.get_lista_leitores():
        for leitor in Init.biblioteca.get_lista_leitores():
            leitor.fechar_banco()
    Init.biblioteca.fechar_banco()


def resize(caminho):
    size = 30, 30

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
        return None
    return im


def gerar_pixel(imagem):
    try:
        pixels = Pixels.from_image(imagem)
        return pixels
    except Exception:
        print(f"Erro ao gerar pixels")
        return None


def is_pyinstaller():
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return True, base_path
    else:
        return False, ""


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
        return f"ERRO, livro '{cod_livro}' não existe"

    if not leitor:
        return f"ERRO, leitor '{email}' não existe"

    emprestimo = Init.biblioteca.emprestar(livro, leitor)
    leitor.atualizar_emprestimos()

    if emprestimo:
        adicao = leitor.add_emprestimo(emprestimo)
        if adicao:
            return f"Livro '{livro.get_titulo()}' emprestado com sucesso"
        else:
            return "ERRO ao adicionar emprestimo ao leitor"
    else:
        return f"ERRO ao emprestar livro '{livro.get_titulo()}', livro não está disponivel"


def devolver(id_emprestimo, email):
    if id_emprestimo == "":
        return "ERRO. ID do Empréstimo está vazio"
    try:
        id_emprestimo = int(id_emprestimo)
    except:
        return f"ERRO ao converter {id_emprestimo}"

    leitor = Init.biblioteca.get_leitor_por_email(email)

    if not leitor:
        return f"ERRO, leitor '{email}' não existe"

    emprestimo = leitor.get_emprestimo_por_id(id_emprestimo)

    if not emprestimo:
        return f"ERRO, empréstimo com id '{id_emprestimo}' não existe"

    livro = emprestimo.get_livro()
    devolucao = Init.biblioteca.devolver(emprestimo)

    if devolucao:
        return f"Livro '{livro.get_titulo()}' devolvido com sucesso"
    else:
        return f"ERRO ao devolver livro '{livro.get_titulo()}' do empréstimo '{id_emprestimo}'"


def cadastrar_livro(dados):
    titulo = dados[0]
    autor = dados[1]
    quant = dados[2]
    caminho_capa = dados[3]
    genero = dados[-1]

    if titulo == "":
        return "ERRO, titulo vazio"

    if autor == "":
        return "ERRO, autor vazio"

    if genero == "":
        return "ERRO, genero vazio"

    if quant == "":
        return "ERRO, quant vazio"

    try:
        quant = int(quant)
    except:
        return f"ERRO ao converter '{quant}'"

    livro = Livro.Livro(titulo, autor, genero, quant)

    if caminho_capa != "":
        livro.set_capa_binaria(caminho_capa)

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
        return "ERRO, email vazio"

    leitor = Leitor.Leitor(nome, email)

    if not leitor:
        return "ERRO ao criar leitor"

    cadastro = Init.biblioteca.add_leitor(leitor)

    if cadastro:
        Init.leitor1 = leitor
        return f"Leitor cadastrado com sucesso\n{leitor}"
    return "ERRO ao cadastrar leitor"


def excluir_leitor(email):

    consulta = Init.biblioteca.get_leitor_por_email(email)

    if not consulta:
        return f"ERRO, Leitor com email '{email}' não existe"

    if email == "":
        return "ERRO. Email do leitor está vazio"

    remocao = Init.biblioteca.remove_leitor(email)
    Init.leitor1 = None

    if remocao:
        return f"Leitor '{email}' removido com sucesso"
    else:
        return f"ERRO, leitor '{email}' não existe"


def excluir_livro(cod_livro):
    if cod_livro == "":
        return "ERRO. Código do livro está vazio"

    try:
        cod_livro = int(cod_livro)
    except:
        return f"ERRO ao converter '{cod_livro}'"

    consulta = Init.biblioteca.get_livro_por_cod(cod_livro)

    if not consulta:
        return f"ERRO, Livro com código '{cod_livro}' não existe"

    remocao = Init.biblioteca.remove_livro(cod_livro)

    if remocao:
        return f"Livro '{cod_livro}' removido com sucesso!"
    else:
        return f"ERRO, não existe livro com código '{cod_livro}'"


def editar_leitor(email, dados):

    if email == "":
        return "ERRO. Email do leitor está vazio"

    leitor = Init.biblioteca.get_leitor_por_email(email)

    if not leitor:
        return f"ERRO, leitor com email '{email}' não existe"

    mensagem = ""

    novo_nome = dados[0]
    novo_email = dados[1]

    if novo_nome != "":
        leitor.set_nome(novo_nome)
        mensagem += f"Nome editado '{novo_nome}'\n"
        Init.biblioteca.atualizar_leitor("nome", leitor.get_email(), novo_nome)
    if novo_email != "":
        if Init.biblioteca.get_leitor_por_email(novo_email):
            mensagem += f"ERRO, '{novo_email}' já cadastrado"
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
        return f"ERRO, não existe livro com código '{cod_livro}'"

    mensagem = ""

    titulo = dados[0]
    autor = dados[1]
    quant = dados[2]
    caminho_capa = dados[3]
    genero = dados[-1]

    if titulo != "":
        livro.set_titulo(titulo)
        mensagem += f"Titulo editado '{titulo}'\n"
        Init.biblioteca.atualizar_livro("titulo", livro.get_codigo(), titulo)
    if autor != "":
        livro.set_autor(autor)
        mensagem += f"Autor editado '{autor}'\n"
        Init.biblioteca.atualizar_livro("autor", livro.get_codigo(), autor)
    if genero != "":
        livro.set_genero(genero)
        mensagem += f"Genero editado '{genero}'\n"
        Init.biblioteca.atualizar_livro("genero", livro.get_codigo(), genero)
    if quant != "":
        try:
            quant = int(quant)
            livro.set_quant(quant)
            mensagem += f"Quant editado '{quant}'"
            Init.biblioteca.atualizar_livro(
                "quantidade", livro.get_codigo(), quant)
        except:
            mensagem += f"ERRO ao converter '{quant}'"

    if caminho_capa != "":
        livro.set_capa_binaria(caminho_capa)

    return mensagem


livro1 = Init.biblioteca.get_livro_por_cod(1)
livro2 = Init.biblioteca.get_livro_por_cod(2)
livro3 = Init.biblioteca.get_livro_por_cod(3)
livro4 = Init.biblioteca.get_livro_por_cod(4)

e_exe, caminho = is_pyinstaller()

if e_exe:
    livro1.set_capa_binaria(f"{caminho}\\assets\\c0.jpg")
    livro2.set_capa_binaria(f"{caminho}\\assets\\c1.jpg")
    livro3.set_capa_binaria(f"{caminho}\\assets\\c2.jpg")
    livro4.set_capa_binaria(f"{caminho}\\assets\\c3.jpg")
else:
    livro1.set_capa_binaria("assets/c0.jpg")
    livro2.set_capa_binaria("assets/c1.jpg")
    livro3.set_capa_binaria("assets/c2.jpg")
    livro4.set_capa_binaria("assets/c3.jpg")

Init.biblioteca.atualizar_livro(
    "capa", livro1.get_codigo(), livro1.get_capa_binaria())
Init.biblioteca.atualizar_livro(
    "capa", livro2.get_codigo(), livro2.get_capa_binaria())
Init.biblioteca.atualizar_livro(
    "capa", livro3.get_codigo(), livro3.get_capa_binaria())
Init.biblioteca.atualizar_livro(
    "capa", livro4.get_codigo(), livro4.get_capa_binaria())

livro1 = Init.biblioteca.get_livro_por_cod(1)
livro2 = Init.biblioteca.get_livro_por_cod(2)
livro3 = Init.biblioteca.get_livro_por_cod(3)
livro4 = Init.biblioteca.get_livro_por_cod(4)
