from model import Leitor, Livro, Biblioteca


class Init:
    usuario_leitor = False
    leitor_cadastado = False

    biblioteca = Biblioteca.Biblioteca()
    leitor1 = Leitor.Leitor("LUCAS", "LUCAS@EMAIL.COM")
    leitor2 = Leitor.Leitor("LEO", "LEO@EMAIL.COM")

    biblioteca.add_leitor(leitor1)
    biblioteca.add_leitor(leitor2)

    livro1 = Livro.Livro("DIARIO DE UM BANANA", "JEFF KINNEY", "HUMOR", 1)
    livro2 = Livro.Livro("O PEQUENO PRÍNCIPE",
                         "ANTOINE DE SAINT-EXUPÉRY", "FÁBULA", 2)
    livro3 = Livro.Livro("1984", "GEORGE ORWELL", "DISTOPIA", 3)
    livro4 = Livro.Livro("1985", "GEORGE ORWELL", "DISTOPIA", 3)
    livro5 = Livro.Livro("1986", "GEORGE ORWELL", "AVENTURA", 3)

    # livro4 = Livro.Livro("O SENHOR DOS ANÉIS", "J.R.R. TOLKIEN", "FANTASIA", 4)
    # livro5 = Livro.Livro("DOM CASMURRO", "MACHADO DE ASSIS", "ROMANCE", 5)
    livro6 = Livro.Livro("A CULPA É DAS ESTRELAS", "JOHN GREEN", "DRAMA", 6)


    biblioteca.add_livro(livro1)
    biblioteca.add_livro(livro2)
    biblioteca.add_livro(livro3)
    biblioteca.add_livro(livro4)
    biblioteca.add_livro(livro5)
    biblioteca.add_livro(livro6)

    leitor1.add_emprestimo(biblioteca.emprestar(livro1, leitor1))
    leitor1.add_emprestimo(biblioteca.emprestar(livro2, leitor1))
