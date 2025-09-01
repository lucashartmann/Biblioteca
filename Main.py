from view.App import App
from controller import Controller
import sys

comando = sys.argv[1:]

# pyinstaller --icon=assets/livros.ico --add-data "assets;assets" --add-data "data;data" --add-data "view/css;view/css" --add-data "view/TelasAdmin/css;view/TelasAdmin/css" --add-data "view/TelasLeitor/css;view/TelasLeitor/css" --add-data "model/Emprestimo.py;model" --hidden-import textual.widgets._tab_pane --name Biblioteca Main.py

# Comandos:
# python Main.py cadastrar_leitor "pedro" "pedro@email.com"
# python Main.py editar_leitor "lucas@email.com" "pedro" "pedro@email.com"
# python Main.py remover_leitor "lucas@email.com"
# python Main.py devolver 1 "lucas@email.com"
# python Main.py retirar 1 "lucas@email.com"
# python Main.py cadastrar_livro "Maus" "Art Spiegelman" 2 "HQ"
# python Main.py editar_livro 1 "Maus" "Art Spiegelman" 2 "HQ"
# python Main.py remover_livro 1


def menu_cmd(comando):
    match comando:
        case ["cadastrar_leitor", nome, email]:
            dados = [nome.upper(), email.upper()]
            print(Controller.cadastrar_leitor(dados))

        case ["editar_leitor", email, novo_nome, novo_email]:
            dados = [novo_nome.upper(), novo_email.upper()]
            print(Controller.editar_leitor(email, dados))

        case ["remover_leitor", email]:
            print(Controller.excluir_leitor(email.upper()))

        case ["devolver", cod_livro, email]:
            print(Controller.devolver(cod_livro, email.upper()))

        case ["retirar", cod_livro, email]:
            print(Controller.emprestar(cod_livro, email.upper()))

        case ["cadastrar_livro", titulo, autor, quant, genero]:
            dados = [titulo.upper(), autor.upper(), genero.upper(), quant]
            print(Controller.cadastrar_livro(dados))

        case ["editar_livro", cod_livro, titulo, autor, quant, genero]:
            dados = [titulo.upper(), autor.upper(), genero.upper(), quant]
            print(Controller.editar_livro(cod_livro, dados))

        case ["remover_livro", cod_livro]:
            print(Controller.excluir_livro(cod_livro))


if __name__ == "__main__":
    if comando:
        menu_cmd(comando)
    else:
        app = App()
        app.run()
