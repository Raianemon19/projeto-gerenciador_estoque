# =====================================
# IMPORTAÇÕES
# =====================================

# Biblioteca usada para trabalhar com banco de dados SQLite
import sqlite3

# Biblioteca usada para manipular caminhos e arquivos do sistema
import os

# Biblioteca usada para criptografar a senha usando hash
import hashlib

# Função que oculta a senha enquanto o usuário digita
from getpass import getpass


# =====================================
# CONEXÃO COM BANCO
# =====================================

# Cria o caminho completo do banco de dados "estoque.db"
# O banco será criado na mesma pasta do arquivo Python
caminho_banco = os.path.join(os.path.dirname(__file__), "estoque.db")


# Cria conexão com o banco de dados
conexao = sqlite3.connect(caminho_banco)

# Cria um cursor para executar comandos SQL
cursor = conexao.cursor()


# =====================================
# CRIAÇÃO DA TABELA
# =====================================

def criar_tabela():

    # Executa um comando SQL
    # Cria a tabela "produtos" caso ela ainda não exista
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (

        --ID único do produto
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        --Nome do produto
        nome TEXT NOT NULL ,

        --Categoria do produto
        categoria TEXT NOT NULL,

        --Preço do produto
        preco REAL NOT NULL,

        --Quantidade disponível no estoque
        quantidade INTEGER NOT NULL,

        --Quantidade mínima permitida em estoque
        estoque_minimo INTEGER NOT NULL,
        
        usuario_id INTEGER NOT NULL,

        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
    )
    """)

    # Salva as alterações no banco
    conexao.commit()


def criar_tabela_usuarios():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL UNIQUE,

        senha TEXT NOT NULL
    )
    """)

    conexao.commit()


# =====================================
# CORES ANSI
# =====================================

# Código ANSI usado para resetar a cor do terminal
RESET = "\033[m"

# Cores utilizadas no terminal
VERMELHO = "\033[1;31m"
VERDE = "\033[1;32m"
AMARELO = "\033[1;33m"
AZUL = "\033[1;34m"
CIANO = "\033[1;36m"
BRANCO = "\033[1;37m"
CINZA = "\033[1;90m"
LILAS = "\033[1;35m"


# =====================================
# FUNÇÕES DE USUÁRIO
# =====================================

def gerar_hash(senha):

    # Converte a senha em hash SHA-256
    # Isso protege a senha no banco de dados
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar_usuario():

    # Exibe título formatado
    print(f"\n{CIANO}=== CADASTRO ==={RESET}")

    # Aviso de segurança
    print(f"{VERMELHO}🔒 Por segurança, sua senha não ficará visível enquanto é digitada.{RESET}")

    # Solicita nome do usuário
    nome = input("Nome: ")

    # Solicita senha sem mostrar no terminal
    senha = getpass("Senha: ")

    # Procura usuário com o mesmo nome
    cursor.execute(
        "SELECT * FROM usuarios WHERE nome = ?",
        (nome,)
    )

    # Verifica se o usuário já existe
    if cursor.fetchone():
        print("Usuário já existe.")
        return

    # Gera hash da senha
    senha_hash = gerar_hash(senha)

    # Insere o novo usuário no banco
    cursor.execute("""
    INSERT INTO usuarios (nome, senha)
    VALUES (?, ?)
    """, (nome, senha_hash))

    # Salva alterações
    conexao.commit()

    # Mensagem de sucesso
    print(f"{VERDE}Usuário cadastrado!{RESET}")


def fazer_login():

    # Exibe título
    print(f"\n{CIANO}=== LOGIN ==={RESET}")

    # Solicita nome
    nome = input("Nome: ")

    # Solicita senha
    senha = getpass("Senha: ")

    # Gera hash da senha
    senha_hash = gerar_hash(senha)

    # Busca usuário no banco
    cursor.execute("""
    SELECT * FROM usuarios
    WHERE nome = ? AND senha = ?
    """, (nome, senha_hash))

    usuario = cursor.fetchone()

    # Verifica se encontrou usuário
    if usuario:

        print(f"{VERDE}Login realizado!{RESET}")

        # Pega ID do usuário
        usuario_id = usuario[0]

        # Verifica estoque baixo
        verificar_estoque_baixo(usuario_id)

        # Retorna ID do usuário logado
        return usuario_id

    else:

        print(f"{VERMELHO}Usuário ou senha inválidos.{RESET}")

        return None


# =====================================
# FUNÇÕES DE CADASTRO
# =====================================

def cadastrar_produto(usuario_id) -> None:
    """Cadastra um novo produto no banco de dados."""

    print(f"\n{CIANO}========= CADASTRO DE PRODUTO ========={RESET}")

    # Remove espaços extras digitados
    nome = input("Digite o nome do produto: ").strip()
    categoria = input("Digite a categoria do produto: ").strip()

    # Verifica se nome ficou vazio
    if not nome:
        print(f"\n{VERMELHO}[ERRO] O nome do produto não pode ficar vazio.{RESET}\n")
        return

    # Verifica se categoria ficou vazia
    if not categoria:
        print(f"\n{VERMELHO}[ERRO] A categoria não pode ficar vazia.{RESET}\n")
        return

    try:

        # Converte preço para float
        preco = float(input("Digite o preço do produto: R$ "))

        # Converte quantidade para inteiro
        quantidade = int(input("Digite a quantidade do produto: "))

        # Converte estoque mínimo para inteiro
        estoque_minimo = int(input("Digite o estoque mínimo: "))
        

        # Verifica se existem valores negativos
        if preco < 0 or quantidade < 0 or estoque_minimo < 0:
            print(f"\n{VERMELHO}[ERRO] Valores não podem ser negativos.{RESET}\n")
            return

    # Erro caso usuário digite letras ao invés de números
    except ValueError:
        print(f"\n{VERMELHO}[ERRO] Digite valores válidos.{RESET}\n")
        return

    try:

        # Insere produto no banco
        cursor.execute("""
            INSERT INTO produtos (
                nome,
                categoria,
                preco,
                quantidade,
                estoque_minimo,
                usuario_id
            )
           VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                categoria,
                preco,
                quantidade,
                estoque_minimo,
                usuario_id

            ))

        # Salva alterações
        conexao.commit()

        print(f"{VERDE}\n✔ Produto cadastrado com sucesso!\n{RESET}")

    # Captura erros do SQLite
    except sqlite3.Error as erro:

        print(f"\n{VERMELHO}[ERRO] Falha ao cadastrar produto: {erro}{RESET}\n")

        # Desfaz alterações caso ocorra erro
        conexao.rollback()
# =====================================
# FUNÇÕES DE ESTOQUE
# =====================================

def listar_produtos(usuario_id) -> None:
    """Lista todos os produtos cadastrados."""

    # Exibe o título da listagem
    print(f"\n{CIANO}========= LISTA DE PRODUTOS ========={RESET}")

    # Executa comando SQL para buscar todos os produtos
    cursor.execute(
    """
        SELECT id, nome, categoria, preco, quantidade, estoque_minimo
        FROM produtos
        WHERE usuario_id = ?
        """,
        (usuario_id,)
)

    # Armazena todos os produtos encontrados
    produtos = cursor.fetchall()

    # Verifica se existem produtos cadastrados
    if not produtos:
        print("\nNenhum produto cadastrado.\n")
        return

    # Percorre cada produto encontrado
    for produto in produtos:
        preco = produto[3]
        quantidade = produto[4]

        valor_total = preco * quantidade

        # Exibe os dados do produto
        print(f"ID: {produto[0]}")
        print(f"Nome: {produto[1]}")
        print(f"Categoria: {produto[2]}")
        print(f"Preço: R$ {produto[3]:.2f}")
        print(f"Quantidade: {produto[4]}")
        print(f"Valor total em estoque: R$ {valor_total:.2f}")
        print(f"Estoque mínimo: {produto[5]}")

        # Linha separadora
        print("-" * 35)


# =====================================
# FUNÇÕES DE ENTRADA E SAÍDA
# =====================================

def registrar_entrada(usuario_id):

    # Exibe título
    print(f"\n{CIANO}======= REGISTRAR ENTRADA ======={RESET}")

    # Mostra lista de produtos disponíveis
    print("Produtos disponíveis:")

    # Busca informações dos produtos no banco
    cursor.execute("""
    SELECT id, nome, quantidade, preco, estoque_minimo
    FROM produtos
    WHERE usuario_id = ?
    """, (usuario_id,))

    # Armazena todos os produtos encontrados
    produtos = cursor.fetchall()

    # Exibe os produtos
    for produto in produtos:

        print(
            f"ID: {produto[0]}, "
            f"Nome: {produto[1]}, "
            f"Quantidade: {produto[2]}, "
            f"Preço: R$ {produto[3]:.2f}, "
            f"Estoque mínimo: {produto[4]}"
        )

    try:

        # Solicita ID do produto
        produto_id = int(input("ID do produto: "))

        # Solicita quantidade de entrada
        quantidade = int(input("Quantidade de entrada: "))

        # Verifica se quantidade é válida
        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            return

    # Captura erro caso usuário digite letras
    except ValueError:
        print("Digite valores numéricos válidos.")
        return

    # Busca o produto pelo ID
    cursor.execute("""
    SELECT * FROM produtos
    WHERE id = ?
    """, (produto_id,))

    # Obtém o produto encontrado
    produto = cursor.fetchone()

    # Verifica se o produto existe
    if produto is None:
        print(f"{VERMELHO}Produto não encontrado.{RESET}")
        return

    # Atualiza a quantidade no estoque
    cursor.execute("""
    UPDATE produtos
    SET quantidade = quantidade + ?
    WHERE id = ?
    """, (quantidade, produto_id))

    # Salva alteração no banco
    conexao.commit()

    # Exibe confirmação
    print(f"Produto: {produto[1]}")
    print(f"{VERDE}Entrada registrada com sucesso!{RESET}")


# ==========================================

def registrar_saida(usuario_id):

    # Exibe título
    print(f"\n{CIANO}======= REGISTRAR SAÍDA ======={RESET}")

    # Mostra os produtos disponíveis
    print("Produtos disponíveis:")

    # Busca os produtos do banco
    cursor.execute("""
    SELECT id, nome, quantidade, preco, estoque_minimo
    FROM produtos
    WHERE usuario_id = ?
    """, (usuario_id,))

    # Armazena os produtos encontrados
    produtos = cursor.fetchall()

    # Exibe os produtos
    for produto in produtos:

        print(
            f"ID: {produto[0]}, "
            f"Nome: {produto[1]}, "
            f"Quantidade: {produto[2]}, "
            f"Preço: R$ {produto[3]:.2f}, "
            f"Estoque mínimo: {produto[4]}"
        )

    try:

        # Solicita ID do produto
        produto_id = int(input("ID do produto: "))

        # Solicita quantidade de saída
        quantidade = int(input("Quantidade de saída: "))

        # Verifica se a quantidade é válida
        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            return

    # Captura erro caso digite letras
    except ValueError:
        print("Digite valores numéricos válidos.")
        return

    # Busca nome e quantidade do produto
    cursor.execute("""
    SELECT nome, quantidade FROM produtos
    WHERE id = ?
    """, (produto_id,))

    # Obtém resultado
    produto = cursor.fetchone()

    # Verifica se produto existe
    if produto is None:
        print(f"{VERMELHO}Produto não encontrado.{RESET}")
        return

    # Armazena nome do produto
    nome = produto[0]

    # Armazena estoque atual
    estoque_atual = produto[1]

    # Verifica se existe quantidade suficiente
    if quantidade > estoque_atual:
        print(f"{VERMELHO}Estoque insuficiente.{RESET}")
        return

    # Atualiza quantidade no banco
    cursor.execute("""
    UPDATE produtos
    SET quantidade = quantidade - ?
    WHERE id = ? AND usuario_id = ?
    """, (quantidade, produto_id, usuario_id))

    # Salva alteração
    conexao.commit()

    # Exibe confirmação
    print(f"Produto: {nome}")
    print(f"{VERDE}Saída registrada com sucesso!{RESET}")


def remover_produto(usuario_id):

    # Exibe título
    print(f"\n{CIANO}======= REMOVER PRODUTO ======={RESET}")

    # Mostra produtos disponíveis
    print("Produtos disponíveis:")

    # Busca produtos cadastrados
    cursor.execute("""
    SELECT id, nome, quantidade, preco, estoque_minimo
    FROM produtos
    WHERE usuario_id = ?
    """, (usuario_id,))

    # Armazena os produtos
    produtos = cursor.fetchall()

    # Exibe os produtos
    for produto in produtos:

        print(
            f"ID: {produto[0]}, "
            f"Nome: {produto[1]}, "
            f"Quantidade: {produto[2]}, "
            f"Preço: R$ {produto[3]:.2f}, "
            f"Estoque mínimo: {produto[4]}"
        )

    try:

        # Solicita ID do produto
        produto_id = int(input("ID do produto: "))

    # Captura erro caso não seja número
    except ValueError:
        print("Digite um ID válido.")
        return

    # Busca o nome do produto
    cursor.execute("""
    SELECT nome FROM produtos
    WHERE id = ? AND usuario_id = ?
    """, (produto_id, usuario_id))

    # Obtém resultado
    produto = cursor.fetchone()

    # Verifica se produto existe
    if produto is None:
        print(f"{VERMELHO}Produto não encontrado.{RESET}")
        return

    # Armazena nome do produto
    nome = produto[0]

    # Remove produto do banco
    cursor.execute("""
    DELETE FROM produtos
    WHERE id = ?
    """, (produto_id,))

    # Salva alteração
    conexao.commit()

    # Exibe confirmação
    print(f"Produto: {nome}")
    print(f"{VERDE}Produto removido com sucesso!{RESET}")


# =====================================
# FUNÇÕES DE ESTOQUE BAIXO
# =====================================

def verificar_estoque_baixo(usuario_id):

    # Busca produtos com estoque menor ou igual ao mínimo
    cursor.execute("""
    SELECT nome, quantidade, estoque_minimo
    FROM produtos
    WHERE quantidade <= estoque_minimo AND usuario_id = ?
    """, (usuario_id,))

    # Armazena os produtos encontrados
    produtos = cursor.fetchall()

    # Verifica se existem produtos com estoque baixo
    if produtos:

        print(f"{AMARELO}⚠ ALERTA DE ESTOQUE ⚠{RESET}")

        # Percorre os produtos encontrados
        for produto in produtos:

            # Armazena dados do produto
            nome = produto[0]
            quantidade = produto[1]
            minimo = produto[2]

            # Exibe alerta
            print(
                f"Produto: {nome} | "
                f"Estoque: {quantidade} | "
                f"Mínimo: {minimo}"
            )

        print("=======================================\n")


# =====================================
# FUNÇÕES DE CONSULTA
# =====================================

def consultar_produto(usuario_id) -> None:

    """Consulta um produto pelo ID."""

    # Exibe título
    print(f"\n{LILAS}========= CONSULTA DE PRODUTO ========={RESET}")

    try:

        # Solicita ID do produto
        produto_id = int(input("Digite o ID do produto: "))

    # Captura erro caso usuário digite texto
    except ValueError:
        print("\n[ERRO] O ID deve ser um número inteiro.\n")
        return

    # Busca produto pelo ID
    cursor.execute(
        """
        SELECT id, nome, categoria, preco, quantidade, estoque_minimo
        FROM produtos
        WHERE id = ? AND usuario_id = ?
    """,
        (produto_id, usuario_id),
    )

    # Obtém resultado da consulta
    produto = cursor.fetchone()

    # Verifica se encontrou produto
    if not produto:
        print("\nProduto não encontrado.\n")
        return

    # Separa os dados em variáveis
    id_prod, nome, categoria, preco, quantidade, estoque_minimo = produto

    # Exibe dados do produto
    print(f"\n{CIANO}========= PRODUTO ENCONTRADO ========={RESET}")
    print(f"ID: {id_prod}")
    print(f"Nome: {nome}")
    print(f"Categoria: {categoria}")
    print(f"Preço: R$ {preco:.2f}")
    print(f"Quantidade: {quantidade}")
    print(f"Estoque mínimo: {estoque_minimo}")
    print("======================================\n")


# =====================================
# MENU
# =====================================

# Executa função para criar tabela de usuários
criar_tabela_usuarios()

# Executa função para criar tabela de produtos
criar_tabela()

# Loop principal do sistema
while True:

    # Exibe menu principal
    print(f' \n{AZUL}========== SISTEMA =========={RESET}')
    print(f"{CIANO}1 - Cadastrar usuário{RESET}")
    print(f"{CIANO}2 - Login{RESET}")
    print(f"{CIANO}3 - Sair{RESET}")
   

    # Solicita opção do usuário
    opcao = input("Escolha: ")

    # Cadastro de usuário
    if opcao == "1":
        cadastrar_usuario()

    # Login do usuário
    elif opcao == "2":
    
   

       # Recebe o ID do usuário logado
        usuario_id = fazer_login()

        # Permite entrar no menu apenas se login for verdadeiro
        if usuario_id:

            # Loop do menu de estoque
            while True:

                # Exibe menu interno
                print(f"\n{LILAS}======= MENU ESTOQUE ======={RESET}")
                print(f"1 -{CIANO} Cadastrar produto{RESET}")
                print(f"2 -{CIANO} Listar produtos{RESET}")
                print(f"3 -{CIANO} Registrar entrada{RESET}")
                print(f"4 -{CIANO} Registrar saída{RESET}")
                print(f"5 -{CIANO} Remover produto{RESET}")
                print(f"6 -{CIANO} Logout{RESET}")

                # Solicita opção
                opcao_estoque = input("Escolha: ")
                # Verifica opção escolhida
                if opcao_estoque == "1":
                    cadastrar_produto(usuario_id)

                elif opcao_estoque == "2":
                    listar_produtos(usuario_id)

                elif opcao_estoque == "3":
                    registrar_entrada(usuario_id)

                elif opcao_estoque == "4":
                    registrar_saida(usuario_id)

                elif opcao_estoque == "5":
                    remover_produto(usuario_id)

                elif opcao_estoque == "6":

                    # Sai do menu interno
                    break

                else:
                    print("Opção inválida.")

    # Encerrar sistema
    elif opcao == "3":
        
    

        # Fecha cursor do banco
        cursor.close()

        # Fecha conexão com banco
        conexao.close()

        print("Sistema encerrado.")

        # Interrompe loop principal
        break

    

    else:
        print("Opção inválida.")


# =====================================
# EXECUÇÃO
# =====================================

# Fecha conexão com banco ao finalizar programa
conexao.close()