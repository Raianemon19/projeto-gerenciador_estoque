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

# =====================================
# FUNÇÕES DE ESTOQUE
# =====================================

# =====================================
# FUNÇÕES DE CONSULTA
# =====================================

# =====================================
# MENU
# =====================================

# =====================================
# EXECUÇÃO
# =====================================
criar_tabela_usuarios() # executa a função
criar_tabela()

conexao.close()