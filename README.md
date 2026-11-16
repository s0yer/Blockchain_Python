# BlockLab • Blockchain Python

Laboratório educacional desktop em Python e Tkinter, com moedas fictícias e persistência local. Não requer pacotes Python externos; o Python precisa incluir Tkinter (`python3-tk` no Ubuntu/Debian).

```bash
python3 Aplicativo.py
```

A interface abre por padrão. Em ambientes sem display, a aplicação usa o console.

## Interface e aprendizado

- **Trilha de aprendizado:** seis etapas com teoria, missões e progresso salvo em `progresso.json`. A introdução é concluída manualmente; as demais etapas são registradas pelas ações no laboratório e no explorador.
- **Laboratório:** escolha a carteira, experimente SHA-256, envie transações, mine blocos e valide a cadeia.
- **Explorador:** selecione um bloco para consultar hashes completos, nonce, data e transações.
- **Painel:** saldo disponível, quantidade de blocos e transações pendentes.

Comece pela trilha. Mine um bloco para receber 100 moedas, envie uma parte para outro nome, mine novamente e inspecione o bloco no explorador. Valide a cadeia para completar a experiência. As etapas podem ser consultadas em qualquer ordem.

O saldo disponível desconta os envios pendentes. Valores não positivos, não finitos, envios para a própria carteira e gastos acima do saldo são recusados. A validação verifica gênesis, índices, vínculos, prova de trabalho, recompensas e saldos históricos. A gravação da cadeia usa substituição atômica e desfaz operações em memória em caso de erro de escrita.

## Escopo educacional

A simulação usa um nó local e dificuldade reduzida (prefixo `00`). Não implementa rede P2P, consenso distribuído, assinaturas digitais, chaves privadas ou taxas. Os nomes identificam carteiras apenas para estudo; não use dados sensíveis ou ativos reais.

A cadeia fica em `blockchain.txt`, junto aos arquivos do projeto, independentemente do diretório de execução. O progresso é separado da cadeia; não apaga transações existentes.

## Verificação

```bash
python3 -m unittest discover -s tests -v
```

Os testes usam arquivos temporários e cobrem mineração, transferências, saldo reservado, valores inválidos, troca de carteira, persistência, adulteração e progresso.

## Executáveis Linux e Windows

Os binários e as instruções para gerar novas versões ficam em [`laucher/`](laucher/README.md). Os executáveis incluem Python e Tkinter; os dados são salvos ao lado de cada binário.
