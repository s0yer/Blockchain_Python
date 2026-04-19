# Blockchain Python

Projeto educacional para simular uma blockchain simples em Python.

## Melhorias aplicadas

- Refatoracao do modulo `Funcoes.py` com persistencia mais robusta.
- Correcao de bug no timestamp do bloco (`bloco.py`).
- Validacoes de transacao e cadeia revisadas.
- Interface grafica desktop com `tkinter/ttk` em `interface_grafica.py`.
- `Aplicativo.py` atualizado para abrir GUI por padrao e fallback em console.

## Como executar

```bash
python Aplicativo.py
```

## Estrutura principal

- `Aplicativo.py`: ponto de entrada.
- `interface_grafica.py`: interface grafica.
- `Funcoes.py`: regras da blockchain (saldo, mineracao, validacao, persistencia).
- `bloco.py` e `transacao.py`: modelos.
- `Hash_util.py`: funcoes de hash.
