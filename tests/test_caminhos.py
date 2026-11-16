import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from caminhos import diretorio_dados


class CaminhosTests(unittest.TestCase):
    def test_executable_data_does_not_use_extraction_directory(self):
        with patch.object(sys, 'frozen', True, create=True), patch.object(sys, 'executable', '/tmp/laucher/BlockLab'):
            self.assertEqual(diretorio_dados(), Path('/tmp/laucher'))

    def test_source_uses_project_directory(self):
        with patch.object(sys, 'frozen', False, create=True):
            self.assertEqual(diretorio_dados(), Path(__file__).resolve().parents[1])
