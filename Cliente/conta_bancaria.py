from customtkinter import *
from rh.funcoes import obter_arquivo
import rh.usuario as user
import app_state as state

# ==================== JANELA ====================

frame_conta = CTkFrame(state.app)
state.frame_conta = frame_conta

# ================= ESTADO GLOBAL =================

entrada_valor_saque = None
popup = None
c1 = None
saldo_label = None
popup_deposito = None
user.openedpop = False
entrada_valor_deposito = None

# ===================== UI =====================

CTkLabel(
    frame_conta,
    text="Conta",
    font=("Arial", 27, "bold")
).pack(pady=(15, 10))

saldo_label = CTkLabel(
    frame_conta,
    text="Saldo: R$ 0.00",
    font=("Arial", 20, "bold")
)
saldo_label.pack(pady=10)

# =================== FUNÇÕES ===================

def extrato(acao: str, valor: float):
    """
    -> Função que imprime o extrato no terminal
    :param acao: se é sacar ou depositar
    :param valor: o valor da ação
    :return: retorna o extrato no terminal
    """
    print("=========== Extrato ===========")
    print(f"Ação: {acao}")
    print(f"Valor: R$ {valor}")
    print("===============================")

def atualizar_saldo():
    """
    -> Função que atualiza o saldo
    :return: retorna o saldo atualizado
    """
    if c1 is None:
        saldo_label.configure(text="R$ 0.00")
        return

    saldo_label.configure(text=f"R$ {c1.saldo:.2f}")

def pegar_saque():
    """
    -> Função que pega o valor do saque no popup
    :return: retorna o valor do saque para o extrato
    """
    global entrada_valor_saque

    try:
        valor = float(entrada_valor_saque.get())

        if c1 and c1.sacar(valor):
            print("Saque realizado com sucesso!")
            atualizar_saldo()
        else:
            print("Saldo insuficiente ou conta não carregada!")

        fechar_popup_sacar()

    except ValueError:
        print("Digite um valor válido.")

def fechar_popup_sacar():
    """
    -> Função que fecha o popup de sacar
    :return: retorna o popup de sacar fechado
    """
    global popup

    user.openedpop = False

    if popup:
        popup.destroy()
        popup = None

def abrir_popup_sacar():
    """
    -> Função que abre o popup de sacar
    :return: retorna o popup de sacar aberto
    """
    global popup
    global entrada_valor_saque

    if user.openedpop:
        return

    user.openedpop = True

    popup = CTkToplevel(state.app)
    popup.protocol("WM_DELETE_WINDOW", fechar_popup_sacar)
    popup.title("Saque")

    largura = 225
    altura = 225

    frame_conta.update_idletasks()

    x = frame_conta.winfo_x() + (frame_conta.winfo_width() // 2) - (largura // 2)
    y = frame_conta.winfo_y() + (frame_conta.winfo_height() // 2) - (altura // 2)

    popup.geometry(f"{largura}x{altura}+{x}+{y}")

    popup.transient(frame_conta)
    popup.grab_set()
    popup.lift()
    popup.focus_force()
    popup.attributes("-topmost", True)

    CTkLabel(
        popup,
        text="Saque",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    entrada_valor_saque = CTkEntry(
        popup,
        placeholder_text="Valor do saque",
        width=175
    )
    entrada_valor_saque.pack(pady=10)

    CTkButton(
        popup,
        text="Confirmar",
        width=175,
        command=pegar_saque
    ).pack(pady=10)

def voltar_menu():
    """
    -> Função que volta para o frame menu
    :return: retorna o frame atual esquecido e abre o frame do menu
    """
    frame_conta.pack_forget()
    state.frame_menu.pack(fill="both", expand=True)

def fechar_popup_depositar():
    """
    -> Função que fecha o popup de depositar
    :return: retorna o popup de depositar fechado
    """
    global popup_deposito

    user.openedpop = False

    if popup_deposito:
        popup_deposito.destroy()
        popup_deposito = None

def pegar_deposito():
    """
    -> Função que pega o valor do deposito no popup
    :return: retorna o valor do deposito para o extrato
    """
    global entrada_valor_deposito

    try:
        valor = float(entrada_valor_deposito.get())

        if c1 and c1.depositar(valor):
            print("Depósito realizado com sucesso!")
            atualizar_saldo()
        fechar_popup_depositar()

    except ValueError:
        print("Digite um valor válido.")

def abrir_popup_depositar():
    """
    -> Função que abre o popup de depositar
    :return: retorna o popup de depositar aberto
    """
    global popup_deposito
    global entrada_valor_deposito

    if user.openedpop:
        return

    user.openedpop = True

    popup_deposito = CTkToplevel(state.app)
    popup_deposito.protocol("WM_DELETE_WINDOW", fechar_popup_depositar)
    popup_deposito.title("Depósito")

    largura = 225
    altura = 225

    frame_conta.update_idletasks()

    x = frame_conta.winfo_x() + (frame_conta.winfo_width() // 2) - (largura // 2)
    y = frame_conta.winfo_y() + (frame_conta.winfo_height() // 2) - (altura // 2)

    popup_deposito.geometry(f"{largura}x{altura}+{x}+{y}")

    popup_deposito.transient(frame_conta)
    popup_deposito.grab_set()
    popup_deposito.lift()
    popup_deposito.focus_force()
    popup_deposito.attributes("-topmost", True)

    CTkLabel(
        popup_deposito,
        text="Depositar",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    entrada_valor_deposito = CTkEntry(
        popup_deposito,
        placeholder_text="Valor do depósito",
        width=175
    )
    entrada_valor_deposito.pack(pady=10)

    CTkButton(
        popup_deposito,
        text="Confirmar",
        width=175,
        command=pegar_deposito
    ).pack(pady=10)

# ==================== CLASSE ====================

class ContaCliente:
    def __init__(self, nome: str, saldo=0):
        self.nome = nome
        self.saldo = saldo

    def sacar(self, saque: float):
        if saque <= self.saldo:
            self.saldo -= saque
            extrato("saque", saque)
            return True
        return False

    def depositar(self, valor):
        self.saldo += valor
        extrato("deposito", valor)
        return True

# ============== CARREGAMENTO DE CONTA ==============

with open(obter_arquivo("login_do_sistema.txt"), "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        linha = linha.strip()

        if not linha:
            continue

        dados = linha.split(";")
        nome = dados[0]

        if len(dados) >= 3 and dados[2] == "cliente":
            c1 = ContaCliente(nome, 1000)  # saldo inicial teste
atualizar_saldo()

# ===================== BOTÕES =====================

CTkButton(
    frame_conta,
    text="Sacar",
    width=200,
    command=abrir_popup_sacar
).pack(pady=10)

CTkButton(
    frame_conta,
    text="Depositar",
    width=200,
    command=abrir_popup_depositar
).pack(pady=5)

# ------------------ BOTÕES Banco ------------------

CTkButton(
    frame_conta,
    text="Voltar",
    width=200,
    command=voltar_menu
).pack(pady=(20, 5))

CTkButton(
    frame_conta,
    text="Sair",
    width=200,
    command=state.app.destroy
).pack(pady=5)
