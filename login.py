from customtkinter import *
import rh.usuario as usuario
from rh.funcoes import obter_arquivo

# Inicializando a janela
Entrada = CTk()

# Título
Entrada.title('Sistema Empresarial')

# Ícone
try:
    Entrada.iconbitmap('empresa.ico')
except:
    pass

# Dimensões da janela
largura = 500
altura = 500

x = (Entrada.winfo_screenwidth() // 2) - (largura // 2)
y = (Entrada.winfo_screenheight() // 2) - (altura // 2)

Entrada.geometry(f'{largura}x{altura}+{x}+{y}')
Entrada.resizable(width=False, height=False)

# _________________ FUNÇÕES _________________

def abrir_menu():
    """
    -> Função que abre o menu principal
    :return: abre o menu principal e fecha a janela atual
    """
    Entrada.destroy()

    try:
        import menu
    except Exception as erro:
        print(erro)
        input()

def fechar_pessoa():
    """
    -> Função para fechar o menu de escolha de usuário
    :return: retorna que está logando
    """
    frame_usuario.pack_forget()
    frame_login.pack(fill="both", expand=True)

def boss():
    """
    -> Função que ativa as opções para a conta chefe
    :return: muda a variável para True e as opções são ativadas
    """
    usuario.chefe = True
    fechar_pessoa()

def func():
    """
    -> Função que ativa as opções para a conta funcionário
    :return: muda a variável para True e as opções são ativadas
    """
    usuario.funcionario = True
    fechar_pessoa()

def client():
    """
    -> Função que ativa as opções para a conta cliente
    :return: muda a variável para True e as opções são ativadas
    """
    usuario.cliente = True
    fechar_pessoa()

def cadastrar():
    """
    -> Função que cadastra o usuário
    :return: retorna os dados inseridos no arquivo de login
    """
    nome = entrada_nome.get().lower().strip()
    senha = entrada_senha.get()

    if nome == "" or senha == "":
        resultado.configure(text="Preencha todos os campos!")
        return

    if len(senha) < 4:
        resultado.configure(text="Crie um senha no minimo 4 digitos!")
        return
    elif len(senha) > 20:
        resultado.configure(text="Crie um senha no máximo 20 digitos!")
        return

    # Verifica se o usuário já existe

    try:
        with open(obter_arquivo("login_do_sistema.txt"), "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if not linha:
                    continue

                dados = linha.split(";")
                usuario_salvo = dados[0]

                if usuario_salvo == nome:
                    resultado.configure(text="Usuário já cadastrado!")
                    return

    except FileNotFoundError:
        pass

    # Salva o novo usuário
    if usuario.cliente:
        with open(obter_arquivo("login_do_sistema.txt"), "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{nome};{senha};cliente\n")

        resultado.configure(text="Cadastro realizado!")
        abrir_menu()
    else:
        with open(obter_arquivo("login_do_sistema.txt"), "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{nome};{senha}\n")

        resultado.configure(text="Cadastro realizado!")
        abrir_menu()

def entrar():
    """
    -> Função que faz o usuário logar com a conta já cadastrada
    :return: pega os dados cadastrados anteriormente no arquivo de login
    """
    nome = entrada_nome.get().lower().strip()
    senha = entrada_senha.get().strip()

    if nome == "" or senha == "":
        resultado.configure(text="Preencha todos os campos!")
        return

    try:
        with open(obter_arquivo("login_do_sistema.txt"), "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if not linha:
                    continue

                dados = linha.split(";")

                usuario = dados[0]
                senha_salva = dados[1]

                if usuario == nome and senha_salva == senha:
                    resultado.configure(text=f"Bem-vindo, {nome}!")
                    abrir_menu()
                    return
                elif usuario == nome and senha_salva != senha:
                    resultado.configure(text='Senha incorreta!')
                    return

        resultado.configure(text="Nome incorreto!")

    except FileNotFoundError:
        resultado.configure(text="Nenhum usuário cadastrado!")

# ================= USUÁRIO =================

# Criação do frame do Usuário
frame_usuario = CTkFrame(
    Entrada,
    fg_color="transparent"
)

# Título
CTkLabel(
    frame_usuario,
    text="Quem está acessando?",
    font=("Arial", 24, "bold")
).pack(pady=(10, 20))

# Botões
CTkButton(
    frame_usuario,
    text="Chefe",
    command=boss,
    width=200
).pack(pady=(20, 10))

CTkButton(
    frame_usuario,
    text="Funcionário",
    command=func,
    width=200
).pack(pady=(20, 10))

CTkButton(
    frame_usuario,
    text="Cliente",
    command=client,
    width=200
).pack(pady=(20, 10))

frame_usuario.pack(fill="both", expand=True)

# ================= LOGIN ==================

# Criação do frame do Login
frame_login = CTkFrame(
    Entrada,
    fg_color="transparent"
)

# Título
CTkLabel(
    frame_login,
    text="Sistema Empresarial",
    font=("Arial", 24, "bold")
).pack(pady=(10, 20))

# Nome
CTkLabel(frame_login, text="Nome").pack(pady=5)

entrada_nome = CTkEntry(frame_login, width=200)
entrada_nome.pack()

# Senha
CTkLabel(frame_login, text="Senha").pack(pady=(15, 5))

entrada_senha = CTkEntry(frame_login, show="*", width=200)
entrada_senha.pack()

# Botões
CTkButton(
    frame_login,
    text="Entrar",
    command=entrar,
    width=200
).pack(pady=(20, 10))

CTkButton(
    frame_login,
    text="Cadastrar",
    command=cadastrar,
    width=200
).pack()

# Mensagem
resultado = CTkLabel(frame_login, text="")
resultado.pack(pady=20)

Entrada.mainloop()
