import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import Funcoes as core
from aprendizado import Progresso


class BlockchainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.patch = patch.object(core, 'ARQUIVO_DADOS', Path(self.temp.name) / 'chain.txt')
        self.patch.start()
        core.proprietario = 'Alice'
        core._inicializa_genesis()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_mining_transfer_reload_and_tampering(self):
        self.assertTrue(core.mine_block())
        self.assertEqual(core.obtem_saldo('Alice'), 100)
        self.assertTrue(core.add_transacao('Bob', valor=30))
        self.assertEqual(core.obtem_saldo('Alice'), 70)
        self.assertFalse(core.add_transacao('Bob', valor=71))
        self.assertTrue(core.verifica_trasacoes())
        self.assertTrue(core.mine_block())
        core.carrega_dados()
        self.assertTrue(core.verifica_chave())
        self.assertEqual(core.obtem_saldo('Bob'), 30)
        core.blockchain[-1].transacoes[-1].valor = 999
        self.assertFalse(core.verifica_chave())
        self.assertFalse(core.mine_block())

    def test_invalid_values_and_dynamic_wallet(self):
        core.mine_block()
        for value in (-1, 0, float('nan'), float('inf'), True):
            self.assertFalse(core.add_transacao('Bob', valor=value))
        self.assertFalse(core.add_transacao(' ', valor=1))
        self.assertFalse(core.add_transacao('Alice', valor=1))
        self.assertTrue(core.add_transacao('Bob', valor=10))
        core.mine_block()
        core.proprietario = 'Bob'
        self.assertTrue(core.add_transacao('Carol', valor=5))
        self.assertEqual(core.transacao_aberta[-1].remetente, 'Bob')

    def test_link_and_genesis_validation(self):
        core.mine_block()
        core.blockchain[-1].hash_anterior = 'alterado'
        self.assertFalse(core.verifica_chave())
        core._inicializa_genesis()
        core.blockchain[0].prova = 0
        self.assertFalse(core.verifica_chave())

    def test_progress_survives_restart(self):
        path = Path(self.temp.name) / 'progress.json'
        progress = Progresso(path)
        progress.concluir('hash')
        self.assertEqual(Progresso(path).concluidas, {'hash'})
        path.write_text('invalid')
        self.assertEqual(Progresso(path).concluidas, set())


if __name__ == '__main__':
    unittest.main()
