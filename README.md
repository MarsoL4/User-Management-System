# User Management System - Database Operations

Bem-vindo ao **User Management System**! Este repositório contém um sistema que facilita o gerenciamento de usuários através da interação com um banco de dados Oracle. Você poderá realizar operações de CRUD (Criar, Ler, Atualizar e Deletar) e também analisar dados de forma simples e intuitiva. O projeto é desenvolvido em Python e utiliza as bibliotecas Pandas e Matplotlib para análise e visualização.


## Estrutura do Projeto

- **`user_management_system.py`**: Este é o script principal, onde você pode cadastrar usuários, editar informações, desativar contas e realizar análises de dados.
- **Banco de Dados Oracle**: Os dados dos usuários são armazenados em uma tabela Oracle, que é acessada e manipulada por meio de comandos SQL.


## Pré-requisitos

Antes de executar o sistema, certifique-se de ter os seguintes itens:

- **Python 3.x**: Certifique-se de ter o Python instalado na sua máquina.
- **Oracle Database**: Você precisará de um banco de dados Oracle em funcionamento.
- **Bibliotecas Python**: Instale as seguintes bibliotecas para que o sistema funcione corretamente:
  - `oracledb`
  - `pandas`
  - `matplotlib`


## Como Executar

Siga estas etapas simples para rodar o sistema:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/user-management-system.git

2. **Instale as dependências**: Execute o seguinte comando no terminal:
   ```python
   pip install oracledb pandas matplotlib

3. **Configure suas credenciais de acesso ao banco de dados:**
  Abra o arquivo user_management_system.py e localize a linha de conexão. Substitua os valores de SEU_USUARIO, SUA_SENHA, SEU_HOST_NAME, SUA_PORTA e SEU_SID conforme necessário:
   ```python
   conn = oracledb.connect(user="SEU_USUARIO", password="SUA_SENHA", dsn="SEU_HOST_NAME:SUA_PORTA/SEU_SID")

4. **Crie a tabela de usuários.** Caso a tabela TBL_USUARIOS não esteja criada no seu banco de dados, utilize o script SQL `criacao-tbl_usuarios.sql` inserido repositório para criá-la

5. **Execute o Programa:** No terminal, execute o seguinte comando para iniciar o sistema:
   ```bash
   python user_management_system.py

## Contribuições
  Sinta-se à vontade para contribuir! Se você encontrar algum problema ou tiver sugestões de melhorias, fique à vontade para abrir uma issue ou enviar um pull request.
