from time import time


class Bloco:
    def __init__(self, indice, hash_anterior, transacoes, prova, selo_tempo=None):
        self.indice = indice
        self.hash_anterior = hash_anterior
        self.seloTempo = time() if selo_tempo is None else selo_tempo
        self.transacoes = transacoes
        self.prova = prova

