import tkinter as tk
from tkinter import messagebox, ttk

import Funcoes


class BlockchainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blockchain Python")
        self.geometry("900x560")
        self.minsize(860, 520)

        Funcoes.carrega_dados()
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        top = ttk.Frame(container)
        top.pack(fill="x")

        self.owner_var = tk.StringVar(value=Funcoes.proprietario)
        ttk.Label(top, text="Proprietario:").pack(side="left")
        ttk.Entry(top, textvariable=self.owner_var, width=18).pack(side="left", padx=6)
        ttk.Button(top, text="Aplicar", command=self._set_owner).pack(side="left")

        self.saldo_var = tk.StringVar(value="Saldo: 0.00")
        self.status_var = tk.StringVar(value="Pronto")
        ttk.Label(top, textvariable=self.saldo_var).pack(side="right")

        form = ttk.LabelFrame(container, text="Nova transacao", padding=10)
        form.pack(fill="x", pady=10)

        self.dest_var = tk.StringVar()
        self.valor_var = tk.StringVar()
        ttk.Label(form, text="Destinatario").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.dest_var, width=28).grid(
            row=0, column=1, padx=8, sticky="w"
        )
        ttk.Label(form, text="Valor").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.valor_var, width=14).grid(
            row=0, column=3, padx=8, sticky="w"
        )
        ttk.Button(form, text="Adicionar", command=self._add_tx).grid(row=0, column=4, padx=8)
        ttk.Button(form, text="Minerar bloco", command=self._mine).grid(row=0, column=5, padx=8)
        ttk.Button(form, text="Validar cadeia", command=self._validate_chain).grid(
            row=0, column=6, padx=8
        )

        mid = ttk.Panedwindow(container, orient="horizontal")
        mid.pack(fill="both", expand=True)

        tx_frame = ttk.LabelFrame(mid, text="Transacoes abertas", padding=8)
        self.tx_list = tk.Listbox(tx_frame, height=10)
        self.tx_list.pack(fill="both", expand=True)
        mid.add(tx_frame, weight=1)

        chain_frame = ttk.LabelFrame(mid, text="Blockchain", padding=8)
        columns = ("indice", "hash_anterior", "prova", "transacoes")
        self.chain_table = ttk.Treeview(chain_frame, columns=columns, show="headings", height=15)
        self.chain_table.heading("indice", text="Indice")
        self.chain_table.heading("hash_anterior", text="Hash anterior")
        self.chain_table.heading("prova", text="Prova")
        self.chain_table.heading("transacoes", text="Qtd tx")
        self.chain_table.column("indice", width=60, anchor="center")
        self.chain_table.column("hash_anterior", width=430)
        self.chain_table.column("prova", width=90, anchor="center")
        self.chain_table.column("transacoes", width=90, anchor="center")
        self.chain_table.pack(fill="both", expand=True)
        mid.add(chain_frame, weight=2)

        ttk.Label(container, textvariable=self.status_var).pack(fill="x", pady=(8, 0))

    def _set_owner(self):
        novo_owner = self.owner_var.get().strip()
        if not novo_owner:
            return
        Funcoes.proprietario = novo_owner
        Funcoes.participantes.add(novo_owner)
        self._refresh("Proprietario atualizado")

    def _add_tx(self):
        destinatario = self.dest_var.get().strip()
        valor_texto = self.valor_var.get().strip()
        if not destinatario or not valor_texto:
            messagebox.showwarning("Dados invalidos", "Informe destinatario e valor.")
            return
        try:
            valor = float(valor_texto)
        except ValueError:
            messagebox.showwarning("Valor invalido", "Digite um numero valido.")
            return

        if Funcoes.add_transacao(destinatario, remetente=Funcoes.proprietario, valor=valor):
            self.dest_var.set("")
            self.valor_var.set("")
            self._refresh("Transacao adicionada")
        else:
            messagebox.showerror("Falha", "Saldo insuficiente para transacao.")

    def _mine(self):
        if not Funcoes.transacao_aberta:
            messagebox.showinfo("Sem transacoes", "Nao ha transacoes abertas para minerar.")
            return
        Funcoes.mine_block()
        self._refresh("Bloco minerado com sucesso")

    def _validate_chain(self):
        valido = Funcoes.verifica_chave()
        if valido:
            messagebox.showinfo("Validacao", "Blockchain valida.")
        else:
            messagebox.showerror("Validacao", "Blockchain invalida.")
        self._refresh()

    def _refresh(self, status=None):
        saldo = Funcoes.obtem_saldo(Funcoes.proprietario)
        self.saldo_var.set("Saldo: {:.2f}".format(saldo))
        self.status_var.set(status or "Pronto")

        self.tx_list.delete(0, tk.END)
        for tx in Funcoes.transacao_aberta:
            self.tx_list.insert(
                tk.END, "{} -> {} ({:.2f})".format(tx.remetente, tx.destinatario, tx.valor)
            )

        for item in self.chain_table.get_children():
            self.chain_table.delete(item)
        for bloco in Funcoes.blockchain:
            self.chain_table.insert(
                "",
                tk.END,
                values=(
                    bloco.indice,
                    bloco.hash_anterior[:64],
                    bloco.prova,
                    len(bloco.transacoes),
                ),
            )


def iniciar_interface():
    app = BlockchainApp()
    app.mainloop()
