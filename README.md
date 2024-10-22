# User Management System - Database Operations

Este repositório contém um sistema de gerenciamento de usuários que interage com um banco de dados Oracle para realizar operações de CRUD (Create, Read, Update, Delete) e análise de dados. O projeto utiliza Python para manipulação de dados e visualização de análises com Pandas e Matplotlib.

## Estrutura do Projeto

- **user_management_system.py**: Script principal que executa as operações de cadastro de usuários, edição, exclusão e análise de dados.
- **Banco de Dados Oracle**: Conjunto de dados armazenados em uma tabela Oracle, acessada e manipulada através de comandos SQL.

## Pré-requisitos

- Python 3.x
- Oracle Database
- Bibliotecas Python:
  - oracledb
  - pandas
  - matplotlib

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/user-management-system.git

2. Instale as dependências:
   ```bash
   pip install oracledb pandas matplotlib

3. Configure as credenciais de acesso ao banco de dados no arquivo
   ```python
   conn = oracledb.connect(conn = oracledb.connect(user="SEU_USUARIO", password="SUA_SENHA", dsn="SEU_HOST_NAME:SUA_PORTA/SEU_SID")

4. Execute o Programa