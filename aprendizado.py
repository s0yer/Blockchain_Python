"""Trilha educacional e progresso local, independentes da interface."""
import json
from caminhos import diretorio_dados

ETAPAS = [
    ("fundamentos", "01", "Entenda a blockchain", "Uma cadeia de confiança",
     "Blockchain é um registro organizado em blocos ligados pelo hash do bloco anterior. Alterar um registro muda seu hash e quebra o vínculo com o próximo bloco.\n\nNesta simulação há um único nó local. Redes reais também precisam de comunicação entre nós e regras de consenso.",
     "Leia a introdução e marque esta etapa como concluída."),
    ("hash", "02", "Experimente um hash", "Uma impressão digital dos dados",
     "SHA-256 transforma dados em um resumo de 256 bits, exibido como 64 caracteres hexadecimais. A mesma entrada gera o mesmo hash; uma pequena alteração produz um resultado muito diferente.\n\nHash não é criptografia reversível e não comprova sozinho quem criou uma transação.",
     "Abra o laboratório e altere o texto do experimento SHA-256."),
    ("minerar", "03", "Mine seu primeiro bloco", "Trabalho que vira um bloco",
     "A prova de trabalho procura um nonce que faça o hash de uma tentativa começar com 00. O minerador testa números até satisfazer essa regra.\n\nAqui a recompensa é de 100 moedas fictícias por bloco. Você pode minerar um bloco vazio para obter seu primeiro saldo. A dificuldade é reduzida para estudo.",
     "No laboratório, clique em Minerar bloco para receber moedas de estudo."),
    ("transacao", "04", "Envie uma transação", "Da carteira para a fila",
     "Uma transação descreve remetente, destinatário e valor. Antes da mineração ela fica na fila de pendências (mempool). O saldo disponível já desconta os envios pendentes para evitar gastar o mesmo valor duas vezes.\n\nAs carteiras deste projeto são nomes, sem chaves privadas ou assinaturas digitais. Use apenas dados e moedas fictícios.",
     "Com saldo disponível, envie um valor para outro participante."),
    ("confirmar", "05", "Confirme e explore", "O registro entra na cadeia",
     "Ao minerar, as transações pendentes são incluídas em um bloco junto com a recompensa. O hash anterior liga esse bloco ao seu antecessor.\n\nSelecione um bloco no explorador para ver o hash completo, o nonce e as transações. Em redes reais, confirmações adicionais dependem de novos blocos e do consenso.",
     "Mine uma transação pendente e selecione o bloco no explorador."),
    ("validar", "06", "Verifique a integridade", "Confiança por verificação",
     "A validação recalcula os vínculos entre blocos e verifica a prova de trabalho, as recompensas e os saldos. Assim podemos identificar várias alterações indevidas no histórico.\n\nUma cadeia local válida não demonstra consenso distribuído. Este projeto não implementa rede P2P, assinaturas, taxas ou segurança para uso financeiro.",
     "Clique em Validar cadeia para verificar seu histórico local."),
]


class Progresso:
    def __init__(self, caminho=None):
        self.caminho = caminho or diretorio_dados() / "progresso.json"
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
            self.concluidas = set(dados) & {etapa[0] for etapa in ETAPAS} if isinstance(dados, list) else set()
        except (OSError, ValueError, TypeError):
            self.concluidas = set()

    def concluir(self, etapa):
        self.concluidas.add(etapa)
        temporario = self.caminho.with_suffix(".tmp")
        temporario.write_text(json.dumps(sorted(self.concluidas)), encoding="utf-8")
        temporario.replace(self.caminho)
