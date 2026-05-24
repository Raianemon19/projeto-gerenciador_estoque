# =====================================
# IMPORTAÇÕES
# =====================================
import sqlite3

import os

# =====================================
# CONEXÃO COM BANCO
# =====================================

caminho_banco = os.path.join(os.path.dirname(__file__), "estoque.db")

conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

# =====================================
# CRIAÇÃO DA TABELA
# =====================================

def criar_tabela():
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    """)

    conexao.commit()

def criar_tabela_usuarios():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    conexao.commit()

# =====================================
# FUNÇÕES DE USUÁRIO
# =====================================

# =====================================
# FUNÇÕES DE CADASTRO
# =====================================
def cadastrar_produto() -> None:
    """Cadastra um novo produto no banco de dados."""

    print("\n========= CADASTRO DE PRODUTO =========")

    # Recebe os dados do usuário
    nome = input("Digite o nome do produto: ").strip()
    categoria = input("Digite a categoria do produto: ").strip()

    # Validação para impedir nome vazio
    if not nome:
        print("\n[ERRO] O nome do produto não pode ficar vazio.\n")
        return

    try:
        # Converte os valores para os tipos corretos
        preco = float(input("Digite o preço do produto: R$ "))
        quantidade = int(input("Digite a quantidade do produto: "))

        # Impede valores negativos
        if preco < 0 or quantidade < 0:
            print("\n[ERRO] Preço e quantidade não podem ser negativos.\n")
            return

    except ValueError:
        print("\n[ERRO] Digite valores numéricos válidos.\n")
        return

    try:
        # Insere os dados no banco
        cursor.execute(
            """
            INSERT INTO produtos (nome, categoria, preco, quantidade)
            VALUES (?, ?, ?, ?)
        """,
            (nome, categoria, preco, quantidade),
        )

        # Salva no banco
        conexao.commit()

        print("\n✔ Produto cadastrado com sucesso!\n")

    except sqlite3.Error as erro:
        print(f"\n[ERRO] Falha ao cadastrar produto: {erro}\n")

        # Desfaz alterações em caso de erro
        conexao.rollback()
# =====================================
# FUNÇÕES DE ESTOQUE
# =====================================
def listar_produtos() -> None:
    """Lista todos os produtos cadastrados."""

    print("\n========= LISTA DE PRODUTOS =========")

    # Busca todos os produtos
    cursor.execute(
        """
        SELECT id, nome, categoria, preco, quantidade
        FROM produtos
    """
    )

    produtos = cursor.fetchall()

    # Verifica se existem produtos
    if not produtos:
        print("\nNenhum produto cadastrado.\n")
        return

    # Exibe cada produto
    for produto in produtos:
        print(f"ID: {produto[0]}")
        print(f"Nome: {produto[1]}")
        print(f"Categoria: {produto[2]}")
        print(f"Preço: R$ {produto[3]:.2f}")
        print(f"Quantidade: {produto[4]}")
        print("-" * 35)
# =====================================
# FUNÇÕES DE CONSULTA
# =====================================
def consultar_produto() -> None:
    """Consulta um produto pelo ID."""

    print("\n========= CONSULTA DE PRODUTO =========")

    try:
        produto_id = int(input("Digite o ID do produto: "))

    except ValueError:
        print("\n[ERRO] O ID deve ser um número inteiro.\n")
        return

    # Busca o produto no banco
    cursor.execute(
        """
        SELECT id, nome, categoria, preco, quantidade
        FROM produtos
        WHERE id = ?
    """,
        (produto_id,),
    )

    # Pega apenas um resultado
    produto = cursor.fetchone()

    # Verifica se encontrou
    if not produto:
        print("\nProduto não encontrado.\n")
        return

    # Desestrutura os dados
    id_prod, nome, categoria, preco, quantidade = produto

    # Exibe os dados
    print("\n========= PRODUTO ENCONTRADO =========")
    print(f"ID: {id_prod}")
    print(f"Nome: {nome}")
    print(f"Categoria: {categoria}")
    print(f"Preço: R$ {preco:.2f}")
    print(f"Quantidade: {quantidade}")
    print("======================================\n")
# =====================================
# MENU
# =====================================

# =====================================
# EXECUÇÃO
# =====================================
criar_tabela_usuarios() # executa a função
criar_tabela()

conexao.close()