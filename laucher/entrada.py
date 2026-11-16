"""Entrada gráfica dos executáveis distribuídos."""
import sys
from pathlib import Path

# Permite executar esta entrada diretamente durante o desenvolvimento.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    if "--self-test" in sys.argv:
        import tempfile
        import Funcoes
        from aprendizado import Progresso
        from caminhos import diretorio_dados
        import tkinter
        from interface_grafica import BlockchainApp

        with tempfile.TemporaryDirectory() as temporary:
            Funcoes.ARQUIVO_DADOS = Path(temporary) / "blockchain.txt"
            Funcoes._inicializa_genesis()
            assert Funcoes.mine_block()
            assert Funcoes.verifica_chave()
            progress = Progresso(Path(temporary) / "progresso.json")
            progress.concluir("hash")
            assert "hash" in Progresso(progress.caminho).concluidas
            assert diretorio_dados() == Path(sys.executable).resolve().parent
        print("BlockLab self-test OK", flush=True)
        return
    if "--smoke-ui" in sys.argv:
        import tempfile
        import Funcoes
        from unittest.mock import patch
        from aprendizado import Progresso
        import interface_grafica

        with tempfile.TemporaryDirectory() as temporary:
            Funcoes.ARQUIVO_DADOS = Path(temporary) / "blockchain.txt"
            with patch.object(interface_grafica, "Progresso", lambda: Progresso(Path(temporary) / "progresso.json")):
                app = interface_grafica.BlockchainApp()
                app.after(1200, app.destroy)
                app.mainloop()
        print("BlockLab GUI OK", flush=True)
        return
    from interface_grafica import iniciar_interface
    iniciar_interface()


if __name__ == "__main__":
    main()
