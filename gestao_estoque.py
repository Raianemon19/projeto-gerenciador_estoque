import sqlite3

# =====================================
# CONEXÃO COM BANCO
# =====================================

conexao = sqlite3.connect("estoque.db")

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

# =====================================
# EXECUÇÃO
# =====================================

criar_tabela()

print("Banco criado com sucesso!")

conexao.close()