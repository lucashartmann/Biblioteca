import shelve


class Save:

    def salvar_dicionario(self, caminho, chave, dicionario):
        with shelve.open(caminho) as db:
            db[chave] = dicionario

    def carregar(self, caminho, chave):
        with shelve.open(caminho) as db:
            dado = db[chave]
            return (dado)

    def deletar(self, caminho, chave):
        with shelve.open(caminho) as db:
            del db[chave]

    def iterar(self, caminho):
        with shelve.open(caminho) as db:
            for chave in db:
                print(chave, db[chave])
