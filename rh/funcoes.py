import csv
from pathlib import Path

cargos = {'TI', 'Frontend', 'Backend'}
produtos = list()

def carregar_cargos():
    """
    -> Função que carrega e abre os cargos já cadastrados
    :return: os cargos cadastrados
    """
    arquivo = obter_arquivo("cargos.csv")

    # Tratamento de erro - Se o arquivo não existir não dá erro
    if not arquivo.exists():
        return

    # Abertura e leitura do arquivo
    with open(arquivo, "r", encoding="utf-8") as csvfile:
        leitor = csv.reader(csvfile)

        for linha in leitor:
            if linha:
                cargos.add(linha[0])

def obter_arquivo(nome_arquivo):
    """
    -> Função que cria uma pasta para os dados
    :param nome_arquivo: nome do arquivo que vai ser adicionado na pasta
    :return: cria a pasta 'dados' para os dados
    """
    pasta = Path('dados')        # Nome dos cargos
    pasta.mkdir(exist_ok=True)
    return pasta / nome_arquivo

def add_cargo(funcao, descricao = "< sem descrição >", salario = 1000):
    """
    -> Função que adiciona o cargo
    :param funcao: o nome do cargo (o que é ou o que faz)
    :param descricao: descrição do cargo
    :param salario: salário medio de quanto ganha
    :return: salva os dados do cargo
    """
    cargo = {
        'funcao': funcao,
        'descricao': descricao,
        'salario_media': salario
    }

    # Tratamento de erro - Se a função estiver sem nada não dará erro
    if not funcao.strip():
        return 'Função é obrigatório!'

    # Tratamento de erro - Se o salário estiver sem nada não dará erro
    if salario is None:
        return 'Salário é obrigatório!'

    if funcao in cargos:
        return "Esse cargo já existe"

    cargos.add(cargo['funcao'])

    # Abertura e escrita do arquivo
    with open(obter_arquivo("cargos.csv"), "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            cargo['funcao'],
            cargo['descricao'],
            cargo['salario_media']
        ])

    # Retorna o resultado
    return 'Cargo cadastrado com sucesso'

def obter_salario_medio(funcao):
    """
    -> Função que obtem o salario médio cadastrado no cargo
    :param funcao: procurar o salário médio no cargo especifico
    :return: o salário médio
    """
    arquivo = obter_arquivo("cargos.csv")

    if not arquivo.exists():
        return None

    # Abertura e leitura do arquivo de cargos
    with open(arquivo, "r", encoding="utf-8") as csvfile:
        leitor = csv.reader(csvfile)

        for linha in leitor:
            if linha and linha[0] == funcao:
                return linha[2]  # salário médio
    return None

def cadastramento_produtos(nome, preco, codigo):

    produto = {
        'nome': nome,
        'preco': preco,
        'codigo': codigo
    }

    if not nome or not nome.strip():
        return 'O nome é obrigatório.'

    try:
        preco = float(preco)
    except ValueError:
        return 'O preco é obrigatório e deve ser um número.'

    if not codigo.strip():
        return 'O código é obrigatório.'

    produtos.append(produto)

    with open(obter_arquivo("produtos.csv"), "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            produto['nome'],
            produto['preco'],
            produto['codigo']
        ])

    # Retorna o resultado
    return 'Produto cadastrado com sucesso!'
