import dbm
import shelve


def salvar(nome_arquivo, chave, dados):
    with shelve.open(f"data/{nome_arquivo}") as db:
        db[chave] = dados


def carregar(nome_arquivo, chave):
    try:
        with shelve.open(f"data/{nome_arquivo}", flag='r') as db:
            if chave in db:
                return db[chave]
            return None
    except dbm.error:
        return None


def deletar(nome_arquivo, chave):
    with shelve.open(f"data/{nome_arquivo}") as db:
        del db[chave]


def iterar(nome_arquivo):
    with shelve.open(f"data/{nome_arquivo}") as db:
        for chave in db:
            print(chave, db[chave])
