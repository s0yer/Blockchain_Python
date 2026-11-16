# Executáveis BlockLab

Os arquivos de distribuição ficam em:

- `linux/BlockLab`: Linux x86_64, compilado no Ubuntu 22.04 (glibc 2.35).
- `windows/BlockLab.exe`: Windows x64, interface gráfica sem janela de console.

Não é necessário instalar Python para executar os binários.

## Abrir

No Linux, abra um terminal na raiz do projeto:

```bash
./laucher/linux/BlockLab
```

Se a permissão de execução for perdida ao copiar:

```bash
chmod +x laucher/linux/BlockLab
```

No Windows, dê dois cliques em `windows\BlockLab.exe`.

Use uma sessão gráfica. O Linux precisa das bibliotecas gráficas do sistema (X11 ou XWayland); o Python e o Tcl/Tk da aplicação estão incluídos. Distribuições com musl, como Alpine, não são o alvo deste binário.

## Dados

`blockchain.txt` e `progresso.json` são criados ao lado de cada executável. Mantenha-o em uma pasta com permissão de escrita. Os binários começam com uma cadeia nova, sem copiar o histórico do desenvolvimento. Para continuar seu histórico, feche a aplicação e copie seus arquivos de dados para a mesma pasta do executável. Faça uma cópia antes de substituir dados.

Cada sistema tem dados independentes. Ao atualizar o binário, preserve os arquivos de dados.

## Gerar novamente

Após alterar o código, gere novamente os executáveis. Para compilar, é necessário Python com Tkinter e acesso à internet na primeira instalação do PyInstaller.

Linux:

```bash
./laucher/gerar-linux.sh
```

Windows: execute `gerar-windows.bat`. O resultado ficará em `windows\BlockLab.exe`.

Os scripts usam um ambiente virtual em `laucher/build/`, sem instalar pacotes no Python global.

Também estão incluídos os ambientes Docker usados para compilar em Linux. Execute os comandos abaixo na raiz do projeto:

```bash
docker build -t blocklab-linux-builder -f laucher/Dockerfile.linux .
docker run --rm --user "$(id -u):$(id -g)" -e PYINSTALLER_CONFIG_DIR=/tmp/pyinstaller -v "$PWD:/src" blocklab-linux-builder python3 laucher/gerar.py

docker build -t blocklab-windows-builder -f laucher/Dockerfile.windows .
docker run --rm --init -v "$PWD:/src" blocklab-windows-builder xvfb-run -a wine 'C:\Python\python.exe' laucher/gerar.py
```

A versão Windows usa Python para Windows dentro do Wine. A compilação nativa pelo `.bat` também está disponível.

## Verificações desta distribuição

Os dois executáveis passaram em testes isolados de mineração, validação, gravação e leitura do progresso e abertura da interface em display virtual. O executável Linux foi testado no Ubuntu 22.04; o Windows foi testado pelo Wine 9, sem validação em uma instalação nativa do Windows.

As somas de verificação dos binários estão em `SHA256SUMS`. Para conferir no Linux:

```bash
cd laucher
sha256sum -c SHA256SUMS
```
