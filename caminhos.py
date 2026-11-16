"""Dados persistentes ficam fora do diretório temporário do empacotador."""
import sys
from pathlib import Path


def diretorio_dados():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent
