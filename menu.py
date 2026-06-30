from tkinter import messagebox
from customtkinter import *
from rh.funcoes import *
from rh.funcionario import *
from time import sleep as sl
import rh.usuario as user
import app_state as state

carregar_cargos()
carregar_funcionarios()

# Janela principal
app = CTk()
state.app = app
import Cliente.conta_bancaria

# Título
app.title("Sistema Empresarial")

# Dimensões da janela
largura = 500
altura = 500

x = (app.winfo_screenwidth() // 2) - (largura // 2)
y = (app.winfo_screenheight() // 2) - (altura // 2)

app.geometry(f"{largura}x{altura}+{x}+{y}")
app.resizable(False, False)


# Váriaveis
popup = None
popup_pro = None
entrada_funci_pro = None
entrada_senior = None
popup_demitir = None
entrada_funci_demi = None

# Ícone
try:
    app.iconbitmap("empresa.ico")
except:
    pass

# _________________ FUNÇÕES _________________

def abrir_cadastro():
    """
    -> Função para abrir a aba de cadastro
    :return: esquece a aba rh e abre cadastro
    """
    frame_rh.pack_forget()
    frame_cadastro.pack(fill="both", expand=True)

def abrir_cargos():
    """
    -> Função para abrir o frame de cargos
    :return: esquece o frame do rh e abre o frame dos cargos
    """
    frame_rh.pack_forget()
    frame_cargos.pack(fill="both", expand=True)

def abrir_rh():
    """
    -> Função para abrir o frame do rh
    :return: esquece o frame do menu e abre o frame do RH
    """
    frame_menu.pack_forget()
    frame_rh.pack(fill="both", expand=True)

def abrir_produtos():
    """
    -> Função para abrir o frame dos produtos
    :return: esquece o frame do menu e abre o frame dos produtos
    """
    frame_menu.pack_forget()
    frame_produtos.pack(fill="both", expand=True)

def voltar_menu(janela):
    """
    -> Função que volta para o frame do menu
    :return: esquece o frame do rh e abre o frame do menu
    """
    janela.pack_forget()
    frame_menu.pack(fill="both", expand=True)

def voltar_rh(janela ):
    """
    -> Função que volta para o frame do RH
    :param janela: variavel que é usado para voltar para o frame do RH
    :return: esquece o frame atual e abre o frame do RH
    """
    janela.pack_forget()
    frame_rh.pack(fill="both", expand=True)

def cadastrar_funcionario():
    """
    -> Função que cadastra funcionários
    :return: retorna os dados inseridos no arquivos
    """
    nome = entrada_nome.get().strip().lower()
    sexo = entrada_sexo.get()
    funcao = entrada_funcao.get().strip().lower()

    try:
        idade = int(entrada_idade.get())
        salario = float(entrada_salario.get())
    except ValueError:
        messagebox.showerror("Erro", "Idade ou salário inválidos")
        return

    resultado = cadastro(nome, idade, sexo, funcao, salario)

    if resultado == "Funcionário cadastrado com sucesso!":
        messagebox.showinfo(
            "Sucesso ao Cadastrar",
            f"Funcionário cadastrado com sucesso!\nSalário: R$ {formatar_salario(salario)}\nFunção: {funcao}"
        )

        entrada_nome.delete(0, "end")
        entrada_idade.delete(0, "end")
        entrada_salario.delete(0, "end")

        entrada_sexo.set("Masculino")
        entrada_funcao.set(sorted(cargos)[0])

        sl(0.3)
        voltar_rh(frame_cadastro)
    else:
        messagebox.showerror("Erro", resultado)

def fechar_popup():
    """
    -> Função que fecha o popup
    :return: faz a variavel do popup ficar em False e fecha o popup
    """
    global popup

    user.openedpop = False

    if popup:
        sl(0.3)
        popup.grab_release()
        popup.destroy()
        popup = None

def abrir_popup():
    """
    -> Função que abre o popup
    :return: faz a variavel do popup ficar em True e não permite abrir mais de um popup
    """
    global popup

    if not user.openedpop:
        user.openedpop = True

        popup = CTkToplevel(app)
        popup.protocol("WM_DELETE_WINDOW", fechar_popup)
        popup.title("Cargos")

        largura = 350
        altura = 350

        app.update_idletasks()

        x = app.winfo_x() + (app.winfo_width() // 2) - (largura // 2)
        y = app.winfo_y() + (app.winfo_height() // 2) - (altura // 2)

        popup.geometry(f"{largura}x{altura}+{x}+{y}")

        # Faz o popup ficar "preso" ao app
        popup.transient(app)

        # Impede clicar na janela principal
        popup.grab_set()

        # Traz para frente
        popup.lift()
        popup.focus_force()

        # Opcional: sempre acima da principal
        popup.attributes("-topmost", True)

        def cadastrar_cargo_popup():
            """
            -> Função que cadastra os cargos no popup
            :return: retorna os dados inseridos dos cargos num arquivo
            """
            resultado = add_cargo(
                entrada_funcao_cargo.get().title(),
                entrada_descricao.get(),
                entrada_me_salario.get()
            )

            if resultado == "Cargo cadastrado com sucesso":
                entrada_funcao.configure(
                    values=sorted(cargos)
                )

                atualizar_cargos()

                messagebox.showinfo(
                    "Sucesso",
                    resultado,
                    parent=popup
                )

                sl(0.1)
                fechar_popup()  # <- adiciona isso

            else:
                messagebox.showerror(
                    "Erro",
                    resultado,
                    parent=popup
                )

        # Botões no popup
        CTkLabel(
            popup,
            text="Adicione",
            font=("Arial", 27, "bold")
        ).pack(pady=(15, 20))

        entrada_funcao_cargo = CTkEntry(
            popup,
            placeholder_text="Nome",
            width=175
        )
        entrada_funcao_cargo.pack(pady=5)

        entrada_descricao = CTkEntry(
            popup,
            placeholder_text="Descrição",
            width=175
        )
        entrada_descricao.pack(pady=5)

        entrada_me_salario = CTkEntry(
            popup,
            placeholder_text="Média Salárial",
            width=175
        )
        entrada_me_salario.pack(pady=5)

        add = CTkButton(
            popup,
            text="Adicione",
            width=150,
            command=cadastrar_cargo_popup
        )
        add.pack(pady=5)

        fechar = CTkButton(
            popup,
            text="Fechar",
            width=150,
            command=fechar_popup
        )
        fechar.pack(pady=5)

def atualizar_cargos():
    """
    -> Função que atualiza os cargos para serem mostrados
    :return: retorna os cargos atualizados
    """
    # Remove apenas os cards da área rolável
    for widget in scroll_cargos.winfo_children():
        widget.destroy()

    # Recria os cards dentro do ScrollableFrame
    for cargo in sorted(cargos):
        card = CTkFrame(
            scroll_cargos,
            fg_color="#3784B5",
            width=175,
            height=40,
            corner_radius=10
        )

        card.pack(pady=6, padx=10, fill="x")
        card.pack_propagate(False)

        CTkLabel(
            card,
            text=cargo,
            font=("Arial", 16, "bold")
        ).pack(expand=True)

def abrir_promo():
    """
    -> Função para abrir o frame de promoções
    :return: esquece o frame do rh e abre o frame dos promoções
    """
    frame_rh.pack_forget()
    frame_promocoes.pack(fill="both", expand=True)
    atualizar_promocoes()

def atualizar_salario_sugerido(escolha):
    """
    -> Função que sugere o salário médio do cargo
    :param escolha: cargo escolhido
    :return: retorna o salário médio do cargo
    """
    salario = obter_salario_medio(escolha)

    if salario:
        entrada_salario.delete(0, "end")
        entrada_salario.insert(0, salario)

def atualizar_promocoes():
    """
     -> Função que atualiza a lista de funcionários para a promoção
    :return: atualiza a lista de funcionários para a promoção
    """
    for widget in scroll_promocoes.winfo_children():
        widget.destroy()

    for funcionario in funcionarios:
        senior = funcionario.get("senioridade", "")

        card = CTkFrame(
            scroll_promocoes,
            fg_color=cor_senioridade(senior),
            width=175,
            height=40,
            corner_radius=10
        )
        card.pack(pady=6, padx=10, fill="x")
        card.pack_propagate(False)

        CTkLabel(
            card,
            text=funcionario["nome"],
            font=("Arial", 16, "bold")
        ).pack(expand=True)

def abrir_demissoes():
    """
    -> Função para abrir o frame de demissões
    :return: esquece o frame do rh e abre o frame dos demissões
    """
    frame_rh.pack_forget()
    frame_demissoes.pack(fill="both", expand=True)
    atualizar_demissoes()

def atualizar_demissoes():
    """
    -> Função que atualiza a lista de funcionários para a demissão
    :return: atualiza a lista de funcionários para a demissão
    """
    for widget in scroll_demissoes.winfo_children():
        widget.destroy()

    for funcionario in funcionarios:
        senior = funcionario.get("senioridade", "")

        card = CTkFrame(
            scroll_demissoes,
            fg_color=cor_senioridade(senior),
            width=175,
            height=40,
            corner_radius=10
        )

        card.pack(pady=6, padx=10, fill="x")
        card.pack_propagate(False)

        CTkLabel(
            card,
            text=funcionario["nome"],
            font=("Arial", 16, "bold")
        ).pack(expand=True)

        card.pack(pady=6, padx=10, fill="x")
        card.pack_propagate(False)

def fechar_popup_promover():
    """
    -> Função que fecha o popup de promoção
    :return: faz a variavel do popup ficar em False e fecha o popup
    """
    global popup_pro

    user.openedpop_pro = False

    if popup_pro:
        sl(0.3)
        popup_pro.grab_release()
        popup_pro.destroy()
        popup_pro = None

def cadastrar_promo():
    """
    -> Função para cadastrar funcionários numa promoção
    :return: retorna os dados inseridos para os arquivos e uma mensagem com o resultado
    """
    funci = entrada_funci_pro.get().strip().lower()
    senior = entrada_senior.get()

    resultado = promocoes(funci, senior)

    if resultado == 'Promoção adicionada com sucesso!':

        messagebox.showinfo('Sucesso!', resultado, parent=popup_pro)

        carregar_funcionarios()
        atualizar_promocoes()

        sl(0.2)
        fechar_popup_promover()
    else:
        messagebox.showerror(
            'Falha',
            resultado,
            parent=popup_pro
        )

def abrir_popup_promover():
    """
    -> Função que abre o popup de promoção
    :return: faz a variavel do popup ficar em True e não permite abrir mais de um popup
    """
    global popup_pro
    global entrada_funci_pro
    global entrada_senior

    if not user.openedpop_pro:
        user.openedpop_pro = True

        sl(0.2)
        popup_pro = CTkToplevel(app)
        popup_pro.protocol("WM_DELETE_WINDOW", fechar_popup_promover)
        popup_pro.title("Promover")

        largura = 350
        altura = 350

        app.update_idletasks()

        x = app.winfo_x() + (app.winfo_width() // 2) - (largura // 2)
        y = app.winfo_y() + (app.winfo_height() // 2) - (altura // 2)

        popup_pro.geometry(f"{largura}x{altura}+{x}+{y}")

        # Faz o popup ficar "preso" ao app
        popup_pro.transient(app)

        # Impede clicar na janela principal
        popup_pro.grab_set()

        # Traz para frente
        popup_pro.lift()
        popup_pro.focus_force()

        # Opcional: sempre acima da principal
        popup_pro.attributes("-topmost", True)

        CTkLabel(
            popup_pro,
            text="Promoções",
            font=("Arial", 27, "bold")
        ).pack(pady=(15, 20))

        entrada_funci_pro = CTkOptionMenu(
            popup_pro,
            values=[f["nome"] for f in funcionarios],
            width=200,
            height=20,
            fg_color="gray",               # Cor do botão
            button_color="#1F6AA5",        # Cor da seta
            button_hover_color="#144870",  # Cor ao passar o mouse
            text_color="white"             # Cor do texto
        )
        entrada_funci_pro.pack(pady=5)

        entrada_senior = CTkOptionMenu(
            popup_pro,
            values=senioridade,
            width=200,
            height=20,
            fg_color="gray",               # Cor do botão
            button_color="#1F6AA5",        # Cor da seta
            button_hover_color="#144870",  # Cor ao passar o mouse
            text_color="white"             # Cor do texto
        )
        entrada_senior.pack(pady=5)

        CTkButton(
            popup_pro,
            text="Salvar",
            width=200,
            command=cadastrar_promo
        ).pack(pady=7)

        fechar_pro = CTkButton(
            popup_pro,
            text="Fechar",
            width=150,
            command=fechar_popup_promover
        )
        fechar_pro.pack(pady=5)

def cor_senioridade(nivel):
    """
    -> Função que muda as cores dos funcionários segundo sua promoção
    :param nivel: senioridade / promoção
    :return: retorna sua cor
    """
    cores = {
        "Estagiário": "#0000FF",
        "Funcionário": "#FF2C2C",
        "Sub-Chefe": "#008000",
        "Chefe do setor": "#FFA500"
    }
    return cores.get(nivel, "#3784B5")

def fechar_popup_demitir():
    """
    -> Função que fecha o popup de demitir
    :return: fecha o popup de demitir
    """
    global popup_demitir

    user.popup_demitir = False

    if popup_demitir:
        sl(0.3)
        popup_demitir.grab_release()
        popup_demitir.destroy()
        popup_demitir = None

def demitir():
    """
    -> Função que demiti os funcionários
    :return: exclui os funcionários
    """
    global entrada_funci_demi
    global popup_demitir

    nome = entrada_funci_demi.get().strip().lower()

    resultado = demissoes(nome)

    if resultado == 'Funcionário demitido com sucesso!':

        messagebox.showinfo('Sucesso!', resultado, parent=popup_demitir)

        carregar_funcionarios()
        atualizar_demissoes()
        atualizar_promocoes()

        sl(0.2)
        fechar_popup_demitir()
    else:
        messagebox.showerror(
            'Falha',
            resultado,
            parent=popup_demitir
        )

def abrir_popup_demitir():
    """
    -> Função que abre o popup de demitir
    :return: retorna o popup de demitir aberto
    """
    global popup_demitir
    global entrada_funci_demi

    if not user.popup_demitir:
        user.popup_demitir = True

        sl(0.2)
        popup_demitir = CTkToplevel(app)
        popup_demitir.protocol("WM_DELETE_WINDOW", fechar_popup_demitir)
        popup_demitir.title("Demissões")

        largura = 350
        altura = 350

        app.update_idletasks()

        x = app.winfo_x() + (app.winfo_width() // 2) - (largura // 2)
        y = app.winfo_y() + (app.winfo_height() // 2) - (altura // 2)

        popup_demitir.geometry(f"{largura}x{altura}+{x}+{y}")

        # Faz o popup ficar "preso" ao app
        popup_demitir.transient(app)

        # Impede clicar na janela principal
        popup_demitir.grab_set()

        # Traz para frente
        popup_demitir.lift()
        popup_demitir.focus_force()

        # Opcional: sempre acima da principal
        popup_demitir.attributes("-topmost", True)

        CTkLabel(
            popup_demitir,
            text="Demissões",
            font=("Arial", 27, "bold")
        ).pack(pady=(15, 20))

        entrada_funci_demi = CTkOptionMenu(
            popup_demitir,
            values=[f["nome"] for f in funcionarios],
            width=200,
            height=20,
            fg_color="gray",  # Cor do botão
            button_color="#1F6AA5",  # Cor da seta
            button_hover_color="#144870",  # Cor ao passar o mouse
            text_color="white"  # Cor do texto
        )
        entrada_funci_demi.pack(pady=5)

        CTkButton(
            popup_demitir,
            text="Confirmar",
            width=200,
            command=demitir
        ).pack(pady=7)

        fechar_demitir = CTkButton(
            popup_demitir,
            text="Fechar",
            width=150,
            command=fechar_popup_demitir
        )
        fechar_demitir.pack(pady=5)

def abrir_conta():
    """
    -> Função que abre o frame da conta
    :return: retorna o frame da conta aberto
    """
    frame_menu.pack_forget()
    state.frame_conta.pack(fill="both", expand=True)

# ================ MENU =================

# Criação do frame do menu
frame_menu = CTkFrame(app)
state.frame_menu = frame_menu

CTkLabel(
    frame_menu,
    text="Menu",
    font=("Arial", 27, "bold")
).pack(pady=(15, 20))

# ================= PRODUTOS =================

# Criação do frame dos Produtos
frame_produtos = CTkFrame(app)

CTkLabel(
    frame_produtos,
    text='Produtos',
    font=('Arial', 27, 'bold')
).pack(pady=(15, 20))

# Botões Produtos
btn_cadastro_pro = CTkButton(
    frame_produtos,
    text="Cadastro de produtos",
    width=200
)
if user.chefe:
    btn_cadastro_pro.pack(pady=5)

# ================= RH =================

# Criação do frame do RH
frame_rh = CTkFrame(app)

CTkLabel(
    frame_rh,
    text="RH",
    font=("Arial", 27, "bold")
).pack(pady=(15, 20))

# Botões RH
btn_cadastro = CTkButton(
    frame_rh,
    text="Cadastro de funcionários",
    width=200,
    command=abrir_cadastro
)
if user.chefe:
    btn_cadastro.pack(pady=5)

CTkButton(
    frame_rh,
    text="Cargos",
    width=200,
    command=abrir_cargos
).pack(pady=5)

btn_promocoes = CTkButton(
    frame_rh,
    text="Promoções",
    width=200,
    command=abrir_promo
)

if user.chefe or user.funcionario:
    btn_promocoes.pack(pady=5)

btn_demissoes = CTkButton(
    frame_rh,
    text="Demissões",
    width=200,
    command=abrir_demissoes
)

if user.chefe or user.funcionario:
    btn_demissoes.pack(pady=5)

# ================ CADASTRO =================

# Criação do frame do Cadastro
frame_cadastro = CTkFrame(app)

CTkLabel(
    frame_cadastro,
    text="Cadastro de \nfuncionários",
    font=("Arial", 27, "bold")
).pack(pady=(15, 20))

entrada_nome = CTkEntry(
    frame_cadastro,
    placeholder_text="Nome",
    width=200
)
entrada_nome.pack(pady=5)

entrada_idade = CTkEntry(
    frame_cadastro,
    placeholder_text="Idade",
    width=200
)
entrada_idade.pack(pady=5)

CTkLabel(
    frame_cadastro,
    text="Sexo"
).pack()
entrada_sexo = CTkOptionMenu(
    frame_cadastro,
    values=["Masculino", "Feminino"],
    width=200,
    height=20,
    fg_color="gray",          # Cor do botão
    button_color="#1F6AA5",      # Cor da seta
    button_hover_color="#144870",# Cor ao passar o mouse
    text_color="white"           # Cor do texto
)
entrada_sexo.pack(pady=3)

CTkLabel(
    frame_cadastro,
    text="Função"
).pack()
entrada_funcao = CTkOptionMenu(
    frame_cadastro,
    values=sorted(cargos),
    command=atualizar_salario_sugerido,
    width=200,
    height=20,
    fg_color="gray",
    button_color="#1F6AA5",
    button_hover_color="#144870",
    text_color="white"
)
entrada_funcao.pack(pady=3)

entrada_salario = CTkEntry(
    frame_cadastro,
    placeholder_text="Salário",
    width=200
)
entrada_salario.pack(pady=5)

CTkButton(
    frame_cadastro,
    text="Cadastrar",
    width=200,
    command=cadastrar_funcionario
).pack(pady=10)

# ================ CARGO =================

# Frame principal
frame_cargos = CTkFrame(app)

titulo_cargos = CTkLabel(
    frame_cargos,
    text="Cargos",
    font=("Arial", 27, "bold")
)
titulo_cargos.pack(pady=(15, 20))

# Área rolável
scroll_cargos = CTkScrollableFrame(
    frame_cargos,
    width=225,
    height=175
)
scroll_cargos.pack(padx=20, pady=10, fill="both", expand=True)

for cargo in cargos:
    card = CTkFrame(
        scroll_cargos,
        fg_color="#3784B5",
        width=175,
        height=40,
        corner_radius=10
    )
    card.pack_propagate(False)

    CTkLabel(
        card,
        text=cargo,
        font=("Arial", 16, 'bold')
    ).pack(expand=True)


    card.pack(pady=6, padx=10, fill='x')

add_cargos = CTkButton(
    frame_cargos,
    text="Adicionar cargo",
    command=abrir_popup
)

if user.chefe:
    add_cargos.pack(pady=20)

# ================ PROMOÇÕES =================

# Criaçãp do frame de promoções
frame_promocoes = CTkFrame(app)

titulo_promocoes = CTkLabel(
    frame_promocoes,
    text="Promoções",
    font=("Arial", 27, "bold")
)
titulo_promocoes.pack(pady=(15, 20))

# Área rolável
scroll_promocoes = CTkScrollableFrame(
    frame_promocoes,
    width=225,
    height=175
)
scroll_promocoes.pack(padx=20, pady=10, fill="both", expand=True)

for funcionario in funcionarios:
    card = CTkFrame(
        scroll_promocoes,
        fg_color=cor_senioridade(funcionario.get("senioridade", "")),
        width=175,
        height=40,
        corner_radius=10
    )
    card.pack_propagate(False)

    CTkLabel(
        card,
        text=funcionario["nome"],
        font=("Arial", 16, "bold")
    ).pack(expand=True)
    card.pack(pady=6, padx=10, fill="x")

var_promover = CTkButton(
    frame_promocoes,
    text="Promover",
    command=abrir_popup_promover
)

if user.chefe:
    var_promover.pack(pady=20)

# ================ DEMISSÕES =================

# Criaçãp do frame de demissões
frame_demissoes = CTkFrame(app)

titulo_demissoes = CTkLabel(
    frame_demissoes,
    text="Demissões",
    font=("Arial", 27, "bold")
)
titulo_demissoes.pack(pady=(15, 20))

# Área rolável
scroll_demissoes = CTkScrollableFrame(
    frame_demissoes,
    width=225,
    height=175
)
scroll_demissoes.pack(padx=20, pady=10, fill="both", expand=True)

for funcionario in funcionarios:
    card = CTkFrame(
        scroll_demissoes,
        fg_color=cor_senioridade(funcionario.get("senioridade", "")),
        width=140,
        height=25,
        corner_radius=6
    )
    card.pack_propagate(False)

    CTkLabel(
        card,
        text=funcionario["nome"],
        font=("Arial", 10, 'bold')
    ).pack(expand=True)
    card.pack(pady=2, padx=10, fill="x")

var_demitir = CTkButton(
    frame_demissoes,
    text="Demitir",
    command=abrir_popup_demitir
)

if user.chefe:
    var_demitir.pack(pady=20)

# ----------------- BOTÕES MENU -----------------

CTkButton(
    frame_menu,
    text="RH",
    width=200,
    command=abrir_rh
).pack(pady=5)

produtos = CTkButton(
    frame_menu,
    text="Produtos",
    width=200,
    command=abrir_produtos
)
if user.chefe or user.funcionario:
    produtos.pack(pady=5)

conta = CTkButton(
    frame_menu,
    text='Conta',
    width=200,
    command=abrir_conta
)
if user.cliente:
    conta.pack(pady=5)

CTkButton(
    frame_menu,
    text="Vendas",
    width=200
).pack(pady=5)

CTkButton(
    frame_menu,
    text="Financeiro",
    width=200
).pack(pady=5)

CTkButton(
    frame_menu,
    text="Sair",
    width=200,
    command=app.destroy
).pack(pady=(35, 15))

# --------------------- BOTÕES RH ---------------------

CTkButton(
    frame_rh,
    text="Voltar",
    width=200,
    command=lambda: voltar_menu(frame_rh)
).pack(pady=(20, 5))

CTkButton(
    frame_rh,
    text="Sair",
    width=200,
    command=app.destroy
).pack(pady=5)

# Tela inicial
frame_menu.pack(fill="both", expand=True)

# --------------------- BOTÕES PRODUTOS ---------------------

CTkButton(
    frame_produtos,
    text="Voltar",
    width=200,
    command=lambda: voltar_menu(frame_produtos)
).pack(pady=(20, 5))

CTkButton(
    frame_produtos,
    text="Sair",
    width=200,
    command=app.destroy
).pack(pady=5)

# Tela inicial
frame_menu.pack(fill="both", expand=True)

# ----------------- BOTÕES CADASTRO ----------------

CTkButton(
    frame_cadastro,
    text="Voltar",
    width=200,
    command=lambda: voltar_rh(frame_cadastro)
).pack(pady=(20, 5))

CTkButton(
    frame_cadastro,
    text="Sair",
    width=200,
    command=app.destroy
).pack(pady=5)

# ----------------- BOTÕES GARGOS -----------------

btn_voltar_cargos = CTkButton(
    frame_cargos,
    text="Voltar",
    width=200,
    command=lambda: voltar_rh(frame_cargos)
)
btn_voltar_cargos.pack(pady=(20, 5))

btn_sair_cargos = CTkButton(
    frame_cargos,
    text="Sair",
    width=200,
    command=app.destroy
)
btn_sair_cargos.pack(pady=5)

# --------------- BOTÕES PROMOÇÕES ---------------

btn_voltar_promocoes = CTkButton(
    frame_promocoes,
    text="Voltar",
    width=200,
    command=lambda: voltar_rh(frame_promocoes)
)
btn_voltar_promocoes.pack(pady=(20, 5))

btn_sair_promocoes = CTkButton(
    frame_promocoes,
    text="Sair",
    width=200,
    command=app.destroy
)
btn_sair_promocoes.pack(pady=5)

# --------------- BOTÕES DEMISSÕES ---------------

btn_voltar_demissoes = CTkButton(
    frame_demissoes,
    text="Voltar",
    width=200,
    command=lambda: voltar_rh(frame_demissoes)
)
btn_voltar_demissoes.pack(pady=(20, 5))

btn_sair_demissoes = CTkButton(
    frame_demissoes,
    text="Sair",
    width=200,
    command=app.destroy
)
btn_sair_demissoes.pack(pady=5)

app.mainloop()
