import csv
from rh.funcoes import obter_arquivo

funcionarios = list()
senioridade = ['Estagiário' ,'Funcionário', 'Sub-Chefe', 'Chefe do setor']

def cadastro(nome, idade, sexo, funcao, salario):
    """
    -> Função que cadastra o funcionário
    :param nome: Nome do funcionário
    :param idade: Idade do funcionário
    :param sexo: Gênero do funcionário
    :param funcao: Cargo do funcionário
    :param salario: Salário do funcionário
    :return: salva os dados inseridos dos funcionários cadastrados
    """
    funcionario = {
        "nome": nome,
        "idade": idade,
        "sexo": sexo,
        "funcao": funcao,
        "salario": salario,
        'senioridade': None
    }

    # Tratamanto de erro - Se o nome estiver vazio não da erro
    if not nome:
        return "Nome é obrigatório!"

    funcionarios.append(funcionario)

    # Abertura e escrita do arquivo
    with open(obter_arquivo("funcionarios_salvos.csv"), "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([nome, idade, sexo, funcao, salario])
    return "Funcionário cadastrado com sucesso!"

def formatar_salario(valor):
    """
    -> Função que formata o salário e deixa de um jeito mais bonito
    :param valor: salário
    :return: retorna o salário formatado do jeito certo
    """
    valor = float(valor)
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def promocoes(funci, senior):
    arquivo = obter_arquivo("funcionarios_salvos.csv")

    funci = funci.strip().lower()

    linhas = []
    encontrado = False

    with open(arquivo, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)

        for linha in leitor:
            if linha and linha[0].strip().lower() == funci:
                # atualização
                if len(linha) > 5:
                    linha[5] = senior
                else:
                    while len(linha) < 5:
                        linha.append("")
                    linha.append(senior)

                encontrado = True

            linhas.append(linha)

    if not encontrado:
        return "Funcionário não encontrado!"

    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerows(linhas)

    return "Promoção adicionada com sucesso!"

def demissoes(nome):
    arquivo = obter_arquivo("funcionarios_salvos.csv")

    nome = nome.strip().lower()

    linhas = []
    encontrado = False

    with open(arquivo, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)

        for linha in leitor:
            if linha and linha[0].strip().lower() == nome:
                encontrado = True
                continue

            linhas.append(linha)

    if not encontrado:
        return "Funcionário não encontrado!"

    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerows(linhas)

    return "Funcionário demitido com sucesso!"

def carregar_funcionarios():
    arquivo = obter_arquivo("funcionarios_salvos.csv")

    if not arquivo.exists():
        return

    funcionarios.clear()

    with open(arquivo, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)

        for linha in leitor:
            if linha:
                funcionarios.append({
                    "nome": linha[0].title(),
                    "idade": linha[1],
                    "sexo": linha[2],
                    "funcao": linha[3].title(),
                    "salario": linha[4],
                    "senioridade": linha[5] if len(linha) > 5 else ""
                })
