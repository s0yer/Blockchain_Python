"""Interface desktop do laboratório educacional, sem dependências externas."""
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

import Funcoes
import Hash_util
from aprendizado import ETAPAS, Progresso


class BlockchainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BlockLab • Blockchain Python")
        self.geometry("1180x800")
        self.minsize(940, 700)
        self.configure(bg="#101827")
        self.progresso = Progresso()
        self.etapa = 0
        Funcoes.carrega_dados()
        self._style()
        self._build_ui()
        self._refresh()

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background="#101827", foreground="#e5edf7", font=("DejaVu Sans", 10))
        style.configure("TFrame", background="#101827")
        style.configure("TLabel", background="#101827")
        style.configure("Title.TLabel", font=("DejaVu Sans", 24, "bold"))
        style.configure("Subtitle.TLabel", foreground="#9aadc5")
        style.configure("Card.TLabel", font=("DejaVu Sans", 16, "bold"), foreground="#62dfbe")
        style.configure("TButton", padding=(12, 9), background="#25354d")
        style.map("TButton", background=[("active", "#365271")])
        style.configure("Accent.TButton", background="#176d61", foreground="white")
        style.configure("TEntry", fieldbackground="#1c2b41", foreground="white", padding=7)
        style.configure("TNotebook", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(20, 12), background="#1c2b41")
        style.map("TNotebook.Tab", background=[("selected", "#176d61")])
        style.configure("Treeview", background="#172338", fieldbackground="#172338", foreground="#e5edf7", rowheight=32)
        style.configure("Treeview.Heading", background="#25354d", padding=8)
        style.map("Treeview", background=[("selected", "#176d61")])

    def _build_ui(self):
        root = ttk.Frame(self, padding=24)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text="BlockLab", style="Title.TLabel").pack(anchor="w")
        ttk.Label(root, text="Aprenda os fundamentos. Experimente. Verifique cada bloco.", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 16))
        self.stats = tk.StringVar()
        ttk.Label(root, textvariable=self.stats, style="Card.TLabel").pack(anchor="w", pady=(0, 16))
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)
        roadmap = ttk.Frame(self.tabs, padding=18)
        lab = ttk.Frame(self.tabs, padding=18)
        explorer = ttk.Frame(self.tabs, padding=18)
        self.tabs.add(roadmap, text="01  Trilha de aprendizado")
        self.tabs.add(lab, text="02  Laboratório")
        self.tabs.add(explorer, text="03  Explorador")
        self._roadmap(roadmap)
        self._lab(lab)
        self._explorer(explorer)
        self.status = tk.StringVar(value="Pronto para explorar • ambiente local com moedas fictícias")
        ttk.Label(root, textvariable=self.status, style="Subtitle.TLabel", wraplength=1050).pack(anchor="w", pady=(12, 0))

    def _roadmap(self, parent):
        self.progress_text = tk.StringVar()
        ttk.Label(parent, textvariable=self.progress_text).pack(anchor="w")
        self.progress_bar = ttk.Progressbar(parent, maximum=len(ETAPAS))
        self.progress_bar.pack(fill="x", pady=(8, 18))
        body = ttk.Frame(parent)
        body.pack(fill="both", expand=True)
        nav = ttk.Frame(body)
        nav.pack(side="left", fill="y", padx=(0, 24))
        self.step_buttons = []
        for i, etapa in enumerate(ETAPAS):
            button = ttk.Button(nav, command=lambda index=i: self._show_step(index), width=29)
            button.pack(fill="x", pady=(0, 8))
            self.step_buttons.append(button)
        content = ttk.Frame(body)
        content.pack(side="left", fill="both", expand=True)
        self.lesson_title = ttk.Label(content, style="Card.TLabel", wraplength=570)
        self.lesson_title.pack(anchor="w", pady=(4, 12))
        self.lesson = self._text(content, height=12)
        self.lesson.pack(fill="both", expand=True)
        self.mission = ttk.Label(content, wraplength=540, foreground="#62dfbe")
        self.mission.pack(anchor="w", pady=12)
        self.lesson_action = ttk.Button(content, style="Accent.TButton", command=self._lesson_action)
        self.lesson_action.pack(anchor="w")
        self._show_step(0)

    def _text(self, parent, height):
        return tk.Text(parent, height=height, bg="#172338", fg="#dce7f5", relief="flat", wrap="word", padx=14, pady=14, font=("DejaVu Sans", 11), state="disabled", insertbackground="white")

    @staticmethod
    def _write(widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _show_step(self, index):
        self.etapa = index
        key, number, title, subtitle, theory, mission = ETAPAS[index]
        self.lesson_title.configure(text=f"{number} / {subtitle}")
        self._write(self.lesson, theory)
        self.mission.configure(text="SUA MISSÃO\n" + mission)
        self.lesson_action.configure(text="Concluir introdução" if index == 0 else "Abrir explorador" if index == 4 else "Abrir laboratório")
        self._progress()

    def _progress(self):
        total = len(self.progresso.concluidas)
        self.progress_text.set(f"SEU ROADMAP   •   {total} de {len(ETAPAS)} etapas concluídas")
        self.progress_bar["value"] = total
        for button, etapa in zip(self.step_buttons, ETAPAS):
            button.configure(text=f"{'✓' if etapa[0] in self.progresso.concluidas else etapa[1]}  {etapa[2]}")

    def _complete(self, key):
        try:
            self.progresso.concluir(key)
        except OSError:
            self.status.set("Atividade concluída; não foi possível salvar o progresso em disco.")
        self._progress()

    def _lesson_action(self):
        if self.etapa == 0:
            self._complete("fundamentos")
            self._show_step(1)
        else:
            self.tabs.select(2 if self.etapa == 4 else 1)

    def _lab(self, parent):
        wallet = ttk.Frame(parent)
        wallet.pack(fill="x", pady=(0, 16))
        ttk.Label(wallet, text="Carteira ativa").pack(side="left")
        self.owner = tk.StringVar(value=Funcoes.proprietario)
        ttk.Entry(wallet, textvariable=self.owner, width=18).pack(side="left", padx=10)
        ttk.Button(wallet, text="Usar carteira", command=self._set_owner).pack(side="left")
        ttk.Button(wallet, text="Validar cadeia", command=self._validate).pack(side="right")
        ttk.Button(wallet, text="Minerar bloco +100", style="Accent.TButton", command=self._mine).pack(side="right", padx=8)
        ttk.Label(parent, text="Envie moedas de estudo", style="Card.TLabel").pack(anchor="w")
        form = ttk.Frame(parent)
        form.pack(fill="x", pady=10)
        self.dest = tk.StringVar()
        self.amount = tk.StringVar()
        ttk.Label(form, text="Destinatário").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Valor").grid(row=0, column=1, sticky="w", padx=10)
        ttk.Entry(form, textvariable=self.dest, width=28).grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.amount, width=15).grid(row=1, column=1, padx=10)
        ttk.Button(form, text="Enviar para a fila", command=self._add_tx).grid(row=1, column=2)
        ttk.Label(parent, text="Pendências • serão confirmadas na próxima mineração", style="Subtitle.TLabel").pack(anchor="w", pady=(8, 4))
        self.pending = self._text(parent, 4)
        self.pending.pack(fill="both", expand=True)
        ttk.Label(parent, text="Experimento SHA-256", style="Card.TLabel").pack(anchor="w", pady=(16, 6))
        ttk.Label(parent, text="Altere um caractere e compare a impressão digital dos dados.", style="Subtitle.TLabel").pack(anchor="w")
        self.hash_input = tk.StringVar(value="Olá, blockchain!")
        ttk.Entry(parent, textvariable=self.hash_input).pack(fill="x", pady=8)
        self.hash_output = tk.StringVar()
        ttk.Entry(parent, textvariable=self.hash_output, state="readonly").pack(fill="x")
        self.hash_output.set(Hash_util.hash_string_256(self.hash_input.get().encode()))
        self.hash_input.trace_add("write", self._hash_changed)

    def _hash_changed(self, *_):
        self.hash_output.set(Hash_util.hash_string_256(self.hash_input.get().encode()))
        self._complete("hash")

    def _explorer(self, parent):
        ttk.Label(parent, text="Cada bloco conta uma parte da história", style="Card.TLabel").pack(anchor="w", pady=(0, 12))
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        columns = ("indice", "hora", "prova", "tx")
        self.chain_table = ttk.Treeview(frame, columns=columns, show="headings", height=7)
        for col, title in zip(columns, ("Bloco", "Criado em", "Nonce", "Transações")):
            self.chain_table.heading(col, text=title)
            self.chain_table.column(col, width=150, anchor="center")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.chain_table.yview)
        self.chain_table.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.chain_table.pack(fill="both", expand=True)
        self.chain_table.bind("<<TreeviewSelect>>", self._inspect)
        self.details = self._text(parent, 10)
        self.details.pack(fill="both", expand=True, pady=(12, 0))
        self._write(self.details, "Selecione um bloco para inspecionar seus dados e transações.")

    def _set_owner(self):
        name = self.owner.get().strip()
        if not name or name == "MINERACAO":
            messagebox.showwarning("Carteira inválida", "Informe um nome. MINERACAO é reservado.")
            return
        Funcoes.proprietario = name
        Funcoes.participantes.add(name)
        self._refresh("Carteira ativa: " + name)

    def _add_tx(self):
        try:
            value = float(self.amount.get().replace(",", "."))
        except ValueError:
            messagebox.showwarning("Valor inválido", "Informe um número positivo, por exemplo 10,50.")
            return
        try:
            accepted = Funcoes.add_transacao(self.dest.get(), valor=value)
        except OSError as exc:
            messagebox.showerror("Falha ao salvar", str(exc))
            return
        if not accepted:
            messagebox.showwarning("Transação recusada", "Confira o saldo, o destinatário e o valor positivo. Use uma carteira destinatária diferente da sua.")
            return
        self.dest.set("")
        self.amount.set("")
        self._refresh("Transação na fila. Mine um bloco para confirmá-la.")
        self._complete("transacao")

    def _mine(self):
        try:
            mined = Funcoes.mine_block()
        except OSError as exc:
            messagebox.showerror("Falha ao salvar", str(exc))
            return
        if not mined:
            messagebox.showerror("Mineração recusada", "A cadeia ou as transações pendentes são inválidas.")
            return
        self._refresh("Novo bloco minerado • recompensa de 100 moedas fictícias.")
        self._complete("minerar")

    def _validate(self):
        valid = Funcoes.verifica_chave()
        self.status.set("Integridade: cadeia válida." if valid else "Integridade: cadeia inválida. Revise os dados locais.")
        if valid:
            self._complete("validar")
        else:
            messagebox.showerror("Integridade", "A cadeia falhou na verificação.")

    def _inspect(self, _event=None):
        selection = self.chain_table.selection()
        if not selection:
            return
        block = Funcoes.blockchain[int(selection[0])]
        txs = "\n".join(f"  {tx.remetente} → {tx.destinatario}: {tx.valor:g}" for tx in block.transacoes)
        self._write(self.details, f"BLOCO #{block.indice}  •  Nonce: {block.prova}\n\nHash: {Hash_util.hash_bloco(block)}\nAnterior: {block.hash_anterior or 'Nenhum — bloco gênesis'}\n\nTRANSAÇÕES\n{txs or 'Sem transações.'}")
        if any(tx.remetente != "MINERACAO" for tx in block.transacoes):
            self._complete("confirmar")

    def _refresh(self, status=None):
        self.stats.set(f"{Funcoes.obtem_saldo(Funcoes.proprietario):,.2f} moedas disponíveis    /    {len(Funcoes.blockchain)} blocos    /    {len(Funcoes.transacao_aberta)} pendentes")
        self._write(self.pending, "\n".join(f"{tx.remetente} → {tx.destinatario}   •   {tx.valor:g} moedas" for tx in Funcoes.transacao_aberta) or "Fila vazia. Mine para receber saldo ou envie uma transação.")
        self.chain_table.delete(*self.chain_table.get_children())
        for block in Funcoes.blockchain:
            date = datetime.fromtimestamp(block.seloTempo).strftime("%d/%m/%Y %H:%M") if block.indice else "Gênesis"
            self.chain_table.insert("", "end", iid=str(block.indice), values=(f"#{block.indice}", date, block.prova, len(block.transacoes)))
        if status:
            self.status.set(status)


def iniciar_interface():
    BlockchainApp().mainloop()
