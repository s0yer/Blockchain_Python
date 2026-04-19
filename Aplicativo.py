import Funcoes
from interface_grafica import iniciar_interface


def executar_console():
    esperando_entrada = True
    Funcoes.carrega_dados()

    while esperando_entrada:
        print("Escolha a opcao:")
        print("n: Adicionar uma nova transacao")
        print("i: Mostrar blockchain")
        print("p: Mostrar participantes")
        print("m: Minerar um novo bloco")
        print("c: Checar validade das transacoes abertas")
        print("o: Obter saldo do participante")
        print("s: Sair")

        escolha = Funcoes.obtem_escolha_usuario().strip().lower()

        if escolha == "n":
            destinatario, valor = Funcoes.obtem_valor_transacao()
            if Funcoes.add_transacao(destinatario, valor=valor):
                print("Transacao adicionada")
            else:
                print("Falha na transacao")
            print(Funcoes.transacao_aberta)
        elif escolha == "i":
            Funcoes.imprime_blockchain()
        elif escolha == "p":
            print(Funcoes.participantes)
        elif escolha == "m":
            Funcoes.mine_block()
            print("Bloco minerado com sucesso")
        elif escolha == "c":
            if Funcoes.verifica_trasacoes():
                print("Todas transacoes sao validas")
            else:
                print("Existe(m) transacoes invalidas")
        elif escolha == "s":
            esperando_entrada = False
        elif escolha == "o":
            nome = input("Participante: ")
            print(Funcoes.obtem_saldo(nome))
        else:
            print("Entrada invalida")

        if not Funcoes.verifica_chave():
            print("Blockchain invalido!")
            break

        print("Saldo de Jadson: {:6.2f}".format(Funcoes.obtem_saldo("Jadson")))


if __name__ == "__main__":
    try:
        iniciar_interface()
    except Exception:
        # Fallback para modo texto caso a GUI falhe.
        executar_console()
