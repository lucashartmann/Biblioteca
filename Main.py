from view.App import App
from controller import Controller
import sys

comando = sys.argv[1:]


def menu_cmd(comando):
    match comando:
        case ["cadastrar_leitor", nome, cpf, rg, telefone, endereco, email]:
            dados = [nome, cpf, rg, telefone, endereco, email]
            Controller.cadastrar_leitor(dados)

        case ["editar_leitor", email, novo_nome, novo_email]:
            dados = [novo_nome, novo_email]
            Controller.editar_leitor(email, dados)

        case ["remover_leitor", email]:
            Controller.excluir_leitor(email)

        case ["devolver", cod_livro, email]:
            Controller.devolver(cod_livro, email)

        case ["retirar", cod_livro, email]:
            Controller.emprestar(cod_livro, email)

        case ["cadastrar_livro", titulo, autor, genero, quant]:
            dados = [titulo, autor, genero, quant]
            Controller.cadastrar_livro(dados)

        case ["editar_livro", cod_livro, titulo, autor, genero, quant]:
            dados = [titulo, autor, genero, quant]
            Controller.editar_livro(cod_livro, dados)
            
        case ["remover_livro", cod_livro]:
            Controller.excluir_livro(cod_livro)


if __name__ == "__main__":
    if comando:
        menu_cmd(comando)
    else:
        app = App()
        app.run()
