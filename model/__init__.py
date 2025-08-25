from model import Leitor, Livro, Biblioteca, Shelve


class Init:
    usuario_leitor = False
    leitor_cadastado = False

    carregar_biblioteca = Shelve.carregar("Banco.db", "Biblioteca")
    if carregar_biblioteca:
        biblioteca = carregar_biblioteca
    else:
        biblioteca = Biblioteca.Biblioteca()
        livro1 = Livro.Livro("DIARIO DE UM BANANA", "JEFF KINNEY", "HUMOR", 1)
        livro2 = Livro.Livro("O PEQUENO PRÍNCIPE",
                            "ANTOINE DE SAINT-EXUPÉRY", "FÁBULA", 2)
        livro3 = Livro.Livro("1984", "GEORGE ORWELL", "DISTOPIA", 3)
        livro4 = Livro.Livro("O SENHOR DOS ANÉIS", "J.R.R. TOLKIEN", "FANTASIA", 4)
        livro5 = Livro.Livro("DOM CASMURRO", "MACHADO DE ASSIS", "ROMANCE", 5)
        livro6 = Livro.Livro("A CULPA É DAS ESTRELAS", "JOHN GREEN", "DRAMA", 6)

        biblioteca.add_livro(livro1)
        biblioteca.add_livro(livro2)
        biblioteca.add_livro(livro3)
        biblioteca.add_livro(livro4)
        biblioteca.add_livro(livro5)
        biblioteca.add_livro(livro6)

    carregar_leitor = Shelve.carregar("Banco.db", "Leitor")
    if carregar_leitor:
        leitor1 = carregar_leitor
    else:
        if not carregar_biblioteca:
            leitor1 = Leitor.Leitor("LUCAS", "LUCAS@EMAIL.COM")
            leitor2 = Leitor.Leitor("LEO", "LEO@EMAIL.COM")
            biblioteca.add_leitor(leitor1)
            biblioteca.add_leitor(leitor2)
            leitor1.add_emprestimo(biblioteca.emprestar(livro1, leitor1))
            leitor1.add_emprestimo(biblioteca.emprestar(livro2, leitor1))
        else:
            leitor1 = biblioteca.get_leitor_por_email("LUCAS@EMAIL.COM")