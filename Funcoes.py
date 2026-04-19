import json
from pathlib import Path

import Hash_util
from bloco import Bloco
from transacao import Transacao


RECOMPENSA_MINERACAO = 100
ARQUIVO_DADOS = Path("blockchain.txt")

blockchain = []
transacao_aberta = []
proprietario = "Jadson"
participantes = {proprietario}


def _bloco_para_dict(bloco):
    return {
        "indice": bloco.indice,
        "hash_anterior": bloco.hash_anterior,
        "seloTempo": bloco.seloTempo,
        "transacoes": [tx.__dict__ for tx in bloco.transacoes],
        "prova": bloco.prova,
    }


def _dict_para_bloco(bloco_dict):
    transacoes = [
        Transacao(tx["remetente"], tx["destinatario"], tx["valor"])
        for tx in bloco_dict.get("transacoes", [])
    ]
    return Bloco(
        bloco_dict["indice"],
        bloco_dict["hash_anterior"],
        transacoes,
        bloco_dict["prova"],
        bloco_dict.get("seloTempo"),
    )


def _atualiza_participantes():
    global participantes
    nomes = {proprietario}
    for bloco in blockchain:
        for tx in bloco.transacoes:
            nomes.add(tx.remetente)
            nomes.add(tx.destinatario)
    for tx in transacao_aberta:
        nomes.add(tx.remetente)
        nomes.add(tx.destinatario)
    participantes = nomes


def _inicializa_genesis():
    global blockchain
    global transacao_aberta
    blockchain = [Bloco(0, "", [], 100, 0)]
    transacao_aberta = []
    _atualiza_participantes()


def carrega_dados():
    global blockchain
    global transacao_aberta
    if not ARQUIVO_DADOS.exists():
        _inicializa_genesis()
        return

    try:
        with ARQUIVO_DADOS.open(mode="r", encoding="utf-8") as arq:
            conteudo = arq.readlines()
            if len(conteudo) < 2:
                raise ValueError("Arquivo de dados incompleto.")

            blockchain_salva = json.loads(conteudo[0].strip())
            blockchain = [_dict_para_bloco(bloco) for bloco in blockchain_salva]

            tx_abertas = json.loads(conteudo[1].strip())
            transacao_aberta = [
                Transacao(tx["remetente"], tx["destinatario"], tx["valor"])
                for tx in tx_abertas
            ]
            _atualiza_participantes()
    except (IOError, ValueError, KeyError, json.JSONDecodeError):
        _inicializa_genesis()


def salvar_dados():
    try:
        with ARQUIVO_DADOS.open(mode="w", encoding="utf-8") as arq:
            arq.write(json.dumps([_bloco_para_dict(bloco) for bloco in blockchain]))
            arq.write("\n")
            arq.write(json.dumps([tx.__dict__ for tx in transacao_aberta]))
    except IOError:
        return False
    return True


def prova_validade(transacoes, ultimo_hash, prova):
    suposicao = (
        str([tx.dict_ordenado() for tx in transacoes]) + str(ultimo_hash) + str(prova)
    ).encode()
    return Hash_util.hash_string_256(suposicao).startswith("00")


def prova_trabalho():
    ultimo_bloco = blockchain[-1]
    ultimo_hash = Hash_util.hash_bloco(ultimo_bloco)
    prova = 0
    while not prova_validade(transacao_aberta, ultimo_hash, prova):
        prova += 1
    return prova


def verifica_transacao(transacao):
    if transacao.remetente == "MINERACAO":
        return True
    return obtem_saldo(transacao.remetente) >= transacao.valor


def obtem_saldo(participante):
    enviado = sum(
        tx.valor
        for bloco in blockchain
        for tx in bloco.transacoes
        if tx.remetente == participante
    )
    enviado += sum(tx.valor for tx in transacao_aberta if tx.remetente == participante)
    recebido = sum(
        tx.valor
        for bloco in blockchain
        for tx in bloco.transacoes
        if tx.destinatario == participante
    )
    return recebido - enviado


def mine_block():
    ultimo_bloco = blockchain[-1]
    hash_anterior = Hash_util.hash_bloco(ultimo_bloco)
    prova = prova_trabalho()
    recompensa = Transacao("MINERACAO", proprietario, RECOMPENSA_MINERACAO)
    transacoes_bloco = transacao_aberta[:] + [recompensa]

    bloco = Bloco(len(blockchain), hash_anterior, transacoes_bloco, prova)
    blockchain.append(bloco)
    transacao_aberta.clear()
    _atualiza_participantes()
    salvar_dados()
    return True


def obtem_ultimo_valor():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transacao(destinatario, remetente=proprietario, valor=1.0):
    transacao = Transacao(remetente, destinatario, valor)
    if not verifica_transacao(transacao):
        return False
    transacao_aberta.append(transacao)
    _atualiza_participantes()
    salvar_dados()
    return True


def obtem_valor_transacao():
    tx_remetente = input("Entre para quem deseja enviar o valor: ")
    tx_valor = float(input("Entre com o seu valor de transação: "))
    return tx_remetente, tx_valor


def obtem_escolha_usuario():
    return input("Sua escolha: ")


def imprime_blockchain():
    for bloco in blockchain:
        print("Saida do Blockchain:")
        print(_bloco_para_dict(bloco))
    print("-" * 20)


def verifica_chave():
    for indice, bloco in enumerate(blockchain):
        if indice == 0:
            continue
        if bloco.hash_anterior != Hash_util.hash_bloco(blockchain[indice - 1]):
            return False
        if not prova_validade(bloco.transacoes[:-1], bloco.hash_anterior, bloco.prova):
            return False
    return True


def verifica_trasacoes():
    return all(verifica_transacao(tx) for tx in transacao_aberta)


