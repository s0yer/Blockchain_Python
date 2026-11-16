import json
import math
from caminhos import diretorio_dados

import Hash_util
from bloco import Bloco
from transacao import Transacao


RECOMPENSA_MINERACAO = 100
ARQUIVO_DADOS = diretorio_dados() / "blockchain.txt"

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
    temporario = ARQUIVO_DADOS.with_suffix(".tmp")
    try:
        conteudo = json.dumps([_bloco_para_dict(bloco) for bloco in blockchain])
        conteudo += "\n" + json.dumps([tx.__dict__ for tx in transacao_aberta])
        temporario.write_text(conteudo, encoding="utf-8")
        temporario.replace(ARQUIVO_DADOS)
    except OSError as exc:
        raise OSError("Não foi possível salvar a blockchain. Verifique as permissões do arquivo.") from exc
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
    return (
        _valor_valido(transacao.valor)
        and bool(transacao.destinatario.strip())
        and transacao.remetente != "MINERACAO"
        and obtem_saldo(transacao.remetente) >= 0
    )


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
    if not verifica_chave() or not verifica_trasacoes():
        return False
    ultimo_bloco = blockchain[-1]
    hash_anterior = Hash_util.hash_bloco(ultimo_bloco)
    prova = prova_trabalho()
    recompensa = Transacao("MINERACAO", proprietario, RECOMPENSA_MINERACAO)
    transacoes_bloco = transacao_aberta[:] + [recompensa]

    bloco = Bloco(len(blockchain), hash_anterior, transacoes_bloco, prova)
    blockchain.append(bloco)
    pendentes = transacao_aberta[:]
    transacao_aberta.clear()
    try:
        salvar_dados()
    except OSError:
        blockchain.pop()
        transacao_aberta.extend(pendentes)
        raise
    _atualiza_participantes()
    return True


def obtem_ultimo_valor():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def _valor_valido(valor):
    return isinstance(valor, (int, float)) and not isinstance(valor, bool) and math.isfinite(valor) and valor > 0


def add_transacao(destinatario, remetente=None, valor=1.0):
    remetente = proprietario if remetente is None else remetente
    if (not isinstance(destinatario, str) or not destinatario.strip()
            or not isinstance(remetente, str) or not remetente.strip()
            or remetente == "MINERACAO" or remetente == destinatario.strip()
            or not _valor_valido(valor) or obtem_saldo(remetente) < valor):
        return False
    transacao = Transacao(remetente, destinatario.strip(), valor)
    if not verifica_transacao(transacao):
        return False
    transacao_aberta.append(transacao)
    try:
        salvar_dados()
    except OSError:
        transacao_aberta.pop()
        raise
    _atualiza_participantes()
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
    if not blockchain or _bloco_para_dict(blockchain[0]) != _bloco_para_dict(Bloco(0, "", [], 100, 0)):
        return False
    saldos = {}
    for indice, bloco in enumerate(blockchain[1:], 1):
        if bloco.indice != indice or bloco.hash_anterior != Hash_util.hash_bloco(blockchain[indice - 1]):
            return False
        if not bloco.transacoes or not prova_validade(bloco.transacoes[:-1], bloco.hash_anterior, bloco.prova):
            return False
        recompensa = bloco.transacoes[-1]
        if (recompensa.remetente != "MINERACAO" or recompensa.valor != RECOMPENSA_MINERACAO
                or not recompensa.destinatario.strip()):
            return False
        for tx in bloco.transacoes[:-1]:
            if (not _valor_valido(tx.valor) or not tx.destinatario.strip()
                    or tx.remetente == "MINERACAO" or saldos.get(tx.remetente, 0) < tx.valor):
                return False
            saldos[tx.remetente] -= tx.valor
            saldos[tx.destinatario] = saldos.get(tx.destinatario, 0) + tx.valor
        saldos[recompensa.destinatario] = saldos.get(recompensa.destinatario, 0) + recompensa.valor
    return True


def verifica_trasacoes():
    return all(verifica_transacao(tx) for tx in transacao_aberta)


