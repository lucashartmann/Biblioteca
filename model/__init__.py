from model import Leitor, Livro, Biblioteca


class Init:
    usuario_leitor = False
    leitor_cadastado = False

    biblioteca = Biblioteca.Biblioteca()

    if not biblioteca.get_lista_livros():
        livro1 = Livro.Livro("DIARIO DE UM BANANA", "JEFF KINNEY", "HUMOR", 1)
        livro2 = Livro.Livro("O PEQUENO PRÍNCIPE",
                             "ANTOINE DE SAINT-EXUPÉRY", "FÁBULA", 2)
        livro3 = Livro.Livro("1984", "GEORGE ORWELL", "DISTOPIA", 3)
        livro4 = Livro.Livro("O SENHOR DOS ANÉIS",
                             "J.R.R. TOLKIEN", "FANTASIA", 4)
        livro5 = Livro.Livro("DOM CASMURRO", "MACHADO DE ASSIS", "ROMANCE", 5)
        livro6 = Livro.Livro("A CULPA É DAS ESTRELAS",
                             "JOHN GREEN", "DRAMA", 6)

        biblioteca.add_livro(livro1)
        biblioteca.add_livro(livro2)
        biblioteca.add_livro(livro3)
        biblioteca.add_livro(livro4)
        biblioteca.add_livro(livro5)
        biblioteca.add_livro(livro6)

    if not biblioteca.get_lista_leitores():
        leitor1 = Leitor.Leitor("LUCAS", "LUCAS@EMAIL.COM")
        leitor2 = Leitor.Leitor("LEO", "LEO@EMAIL.COM")
        biblioteca.add_leitor(leitor1)
        biblioteca.add_leitor(leitor2)

        livro_um = biblioteca.get_livro_por_cod(1)
        livro_dois = biblioteca.get_livro_por_cod(2)
        livro_tres = biblioteca.get_livro_por_cod(3)

        emprestimo1 = biblioteca.emprestar(livro_um, leitor1)
        emprestimo2 = biblioteca.emprestar(livro_dois, leitor1)
        emprestimo3 = biblioteca.emprestar(livro_tres, leitor2)

        adicao_emprestimo = leitor1.add_emprestimo(emprestimo1)
        adicao_emprestimo1 = leitor2.add_emprestimo(emprestimo3)
        leitor1.add_emprestimo(emprestimo2)
    else:
        leitor1 = biblioteca.get_leitor_por_email("LUCAS@EMAIL.COM")
