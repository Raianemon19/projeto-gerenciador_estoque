📦 Sistema de Gestão de Estoque
📌 Descrição

Sistema desenvolvido em Python para gerenciamento de estoque de produtos, utilizando banco de dados SQLite para armazenamento das informações.

O sistema possui autenticação de usuários com senha criptografada em SHA-256, controle completo de estoque e organização dos produtos por usuário.

🎯 Objetivo

Aplicar conceitos de:

Programação estruturada
Manipulação de dados
Funções em Python
Banco de dados SQLite
CRUD de produtos
Segurança básica com hash de senha
Organização de código
Controle de versão com Git/GitHub

⚙️ Funcionalidades

👤 Usuários
Cadastro de usuários
Login no sistema
Senhas protegidas com criptografia SHA-256
Ocultação de senha com getpass

📦 Produtos
Cadastro de produtos
Consulta de produto por ID
Listagem de produtos
Remoção de produtos
Organização dos produtos por usuário

📊 Controle de Estoque
Entrada de produtos
Saída de produtos
Cálculo do valor total em estoque
Alerta automático de estoque baixo
Definição de estoque mínimo

💾 Banco de Dados
Armazenamento utilizando SQLite
Criação automática das tabelas
Relacionamento entre usuários e produtos
Persistência dos dados em estoque.db

🗂️ Estrutura do Projeto
gestao-estoque/
│
├── .gitignore
├── estoque.db
├── gestao_estoque.py
└── README.md

🛠️ Tecnologias Utilizadas
Python
SQLite3
Hashlib
Getpass
Git
GitHub
VS Code
▶️ Como Executar
1️⃣ Clonar o repositório
git clone https://github.com/Raianemon19/projeto-gerenciador_estoque
2️⃣ Acessar a pasta do projeto
cd projeto-gerenciador_estoque
3️⃣ Executar o sistema
python gestao_estoque.py
🔐 Segurança

O sistema utiliza:

Criptografia SHA-256 para armazenamento de senhas
Ocultação de senha no terminal utilizando getpass
Separação de produtos por usuário autenticado

🧠 Conceitos Aplicados
CRUD
Banco de dados relacional
Relacionamento entre tabelas
Tratamento de erros
Validação de entradas
Modularização com funções
Manipulação de banco SQLite
Segurança básica de autenticação

👥 Integrantes
Arthur Ribeiro Ferreira
Diogo Ribeiro Rodrigues Brauna
Raiane dos Santos de Oliveira
📚 Observações

Projeto desenvolvido para fins acadêmicos, com foco na prática de:

Lógica de programação
Programação em Python
Banco de dados SQLite
Segurança básica de autenticação
Organização e estruturação de sistemas
## 📚 Observações

Projeto desenvolvido para fins acadêmicos, com foco na prática de lógica de programação, organização de código e utilização de banco de dados com Python.
