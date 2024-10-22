# Imports ----------------------------
import os
import oracledb
import pandas as pd
import matplotlib.pyplot as plt

# Subalgoritmos ----------------------
# Cria conexão com o banco de dados
def conectar_bd() -> oracledb.Connection:
    try:
        conn = oracledb.connect(user="SEU_USUARIO", password="SUA_SENHA", dsn="SEU_HOST_NAME:SUA_PORTA/SEU_SID")
        print("Conexão aberta com sucesso!")
        return conn
    except oracledb.DatabaseError as e:
        print(f"Erro de conexão: {e}")
        return None

# Função para listar registros (ativos, desativados ou todos)
def listar_registros(conn: oracledb.Connection, filtro_ativo=None) -> None:
    try:
        query = "SELECT ID, Nome, Idade, Cidade, Profissao, Salario, Nascimento, ATIVO FROM TBL_USUARIOS"
        params = []
        
        if filtro_ativo is not None:
            query += " WHERE ATIVO = :1"
            params.append(filtro_ativo)

        with conn.cursor() as inst_cadastro:
            inst_cadastro.execute(query, params)
            registros = inst_cadastro.fetchall()

            if not registros:
                print("\nNenhum registro encontrado.")
            else:
                for registro in registros:
                    print(registro)
            print("_" * 70)
            input("\nENTER para continuar...")
    except oracledb.DatabaseError as e:
        print(f"Erro ao listar registros: {e}")
        
# Função para listar registros e fazer análise com Pandas
def listar_registros_com_pandas(conn: oracledb.Connection) -> None:
    try:
        with conn.cursor() as cursor:
            # Consultar todos os registros da tabela
            cursor.execute("SELECT ID, Nome, Idade, Cidade, Profissao, Salario, TO_CHAR(Nascimento, 'YYYY-MM-DD'), ATIVO FROM TBL_USUARIOS")
            registros = cursor.fetchall()

            # Verificar se há registros
            if not registros:
                print("\nNenhum registro encontrado.")
                return

            # Criar DataFrame a partir dos dados
            df = pd.DataFrame(registros, columns=['ID', 'Nome', 'Idade', 'Cidade', 'Profissao', 'Salario', 'Nascimento', 'ATIVO'])

            # Exibir relatório de registros
            print("\n" + "=" * 65)
            print("RELATÓRIO DE REGISTROS".center(65))
            print("=" * 65)
            print(df.to_string(index=False))
            print("=" * 65)

            # Análise de idade
            media_idade = df['Idade'].mean()
            print(f"Média de Idade: {media_idade:.2f}")
            print(f"Número de Registros: {len(df)}")
            print("=" * 65)

            # Gerar gráfico de idades
            plt.figure(figsize=(10, 6))
            plt.bar(df['Nome'], df['Idade'], color='skyblue')
            plt.axhline(y=media_idade, color='r', linestyle='--', label=f'Média de Idade: {media_idade:.2f}')
            plt.title('Distribuição de Idade dos Usuários')
            plt.xlabel('Nome')
            plt.ylabel('Idade')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()

            input("\nPressione ENTER para continuar...")
    except oracledb.DatabaseError as e:
        print(f"Erro ao listar registros: {e}")

# Função para adicionar um novo registro
def adicionar_registro(conn: oracledb.Connection) -> None:
    try:
        with conn.cursor() as inst_cadastro:
            nome = input("Nome: ").strip()
            if not nome:
                print("Nome não pode ser vazio.")
                return

            idade = input("Idade: ").strip()
            if not idade.isdigit():
                print("Idade deve ser um número válido.")
                return

            cidade = input("Cidade: ").strip()
            profissao = input("Profissão: ").strip()
            salario = input("Salário: ").strip()
            if not salario.replace('.', '', 1).isdigit():
                print("Salário deve ser um número válido.")
                return

            nascimento = input("Data de Nascimento (AAAA-MM-DD): ").strip()
            try:
                pd.to_datetime(nascimento)  # Validação simples da data
            except ValueError:
                print("Formato de data inválido.")
                return

            ativo = 1  # Considerando que o usuário começa como ativo
            
            query = """
                INSERT INTO TBL_USUARIOS (Nome, Idade, Cidade, Profissao, Salario, Nascimento, ATIVO)
                VALUES (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7)
            """
            inst_cadastro.execute(query, [nome, idade, cidade, profissao, salario, nascimento, ativo])
            conn.commit()
            print("Registro adicionado com sucesso!")
            input("\nENTER para continuar...")
    except oracledb.DatabaseError as e:
        print(f"Erro ao adicionar registro: {e}")

# Função para editar um registro existente
def editar_registro(conn: oracledb.Connection, id_registro: int) -> None:
    try:
        with conn.cursor() as inst_cadastro:
            # Buscar o registro atual
            inst_cadastro.execute("SELECT * FROM TBL_USUARIOS WHERE ID = :1", [id_registro])
            registro = inst_cadastro.fetchone()

            if not registro:
                print("Registro não encontrado.")
                return

            print(f"Registro atual: {registro}")

            # Solicitar novos valores
            novo_nome = input(f"Nome ({registro[1]}): ") or registro[1]
            nova_idade = input(f"Idade ({registro[2]}): ") or registro[2]
            nova_cidade = input(f"Cidade ({registro[3]}): ") or registro[3]
            nova_profissao = input(f"Profissão ({registro[4]}): ") or registro[4]
            novo_salario = input(f"Salário ({registro[5]}): ") or registro[5]
            nova_nascimento = input(f"Nascimento ({registro[6]} - AAAA-MM-DD): ") or registro[6]

            query = """
                UPDATE TBL_USUARIOS
                SET Nome = :1, Idade = :2, Cidade = :3, Profissao = :4, Salario = :5, Nascimento = TO_DATE(:6, 'YYYY-MM-DD')
                WHERE ID = :7
            """
            inst_cadastro.execute(query, [novo_nome, nova_idade, nova_cidade, nova_profissao, novo_salario, nova_nascimento, id_registro])
            conn.commit()
            print("Registro atualizado com sucesso!")
            input("\nENTER para continuar...")
    except oracledb.DatabaseError as e:
        print(f"Erro ao editar registro: {e}")

# Função para desativar (excluir logicamente) um registro
def excluir_registro_logico(conn: oracledb.Connection, id_registro: int) -> None:
    try:
        with conn.cursor() as inst_cadastro:
            inst_cadastro.execute("UPDATE TBL_USUARIOS SET ATIVO = 0 WHERE ID = :1", [id_registro])
            conn.commit()
            print("Registro desativado com sucesso!")
            input("\nENTER para continuar...")
    except oracledb.DatabaseError as e:
        print(f"Erro ao desativar registro: {e}")

# Função para listar registros com opções de filtro
def listar_registros_opcao(conn: oracledb.Connection) -> None:
    print("\nSelecione o tipo de listagem:")
    print("1 - Apenas usuários ATIVOS")
    print("2 - Apenas usuários DESATIVADOS")
    print("3 - Todos os usuários")

    opcao_filtro = input("\nEscolha uma opção: ")
    filtro_ativo = None
    if opcao_filtro == '1':
        filtro_ativo = True
    elif opcao_filtro == '2':
        filtro_ativo = False
    elif opcao_filtro != '3':
        print("Opção inválida.")
        return

    listar_registros(conn, filtro_ativo)
    

# Função para filtrar registros com base em Nome, Salário e Nascimento
def filtrar_registros(conn: oracledb.Connection) -> None:
    print("\nSelecione o campo para filtrar:")
    print("1 - Nome (like)")
    print("2 - Salário")
    print("3 - Nascimento")
    
    opcao = input("\nEscolha uma opção: ")
    
    try:
        with conn.cursor() as inst_cadastro:
            if opcao == '1':
                nome = input("Digite parte do nome para filtrar (use % para curinga): ")
                query = "SELECT * FROM TBL_USUARIOS WHERE Nome LIKE :1"
                inst_cadastro.execute(query, [nome])
            elif opcao == '2':
                print("\nEscolha o tipo de filtro para Salário:")
                print("1 - igual")
                print("2 - maior")
                print("3 - menor")
                print("4 - entre")
                tipo_filtro = input("Escolha uma opção: ")
                
                if tipo_filtro == '1':
                    salario = float(input("Digite o salário: "))
                    query = "SELECT * FROM TBL_USUARIOS WHERE Salario = :1"
                    inst_cadastro.execute(query, [salario])
                elif tipo_filtro == '2':
                    salario = float(input("Digite o salário: "))
                    query = "SELECT * FROM TBL_USUARIOS WHERE Salario > :1"
                    inst_cadastro.execute(query, [salario])
                elif tipo_filtro == '3':
                    salario = float(input("Digite o salário: "))
                    query = "SELECT * FROM TBL_USUARIOS WHERE Salario < :1"
                    inst_cadastro.execute(query, [salario])
                elif tipo_filtro == '4':
                    salario_min = float(input("Digite o salário inicial: "))
                    salario_max = float(input("Digite o salário final: "))
                    query = "SELECT * FROM TBL_USUARIOS WHERE Salario BETWEEN :1 AND :2"
                    inst_cadastro.execute(query, [salario_min, salario_max])
                else:
                    print("Opção inválida.")
                    return
            elif opcao == '3':
                print("\nEscolha o tipo de filtro para Nascimento:")
                print("1 - igual")
                print("2 - maior")
                print("3 - menor")
                print("4 - entre")
                tipo_filtro = input("Escolha uma opção: ")
                
                if tipo_filtro == '1':
                    nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ")
                    query = "SELECT * FROM TBL_USUARIOS WHERE Nascimento = TO_DATE(:1, 'YYYY-MM-DD')"
                    inst_cadastro.execute(query, [nascimento])
                elif tipo_filtro == '2':
                    nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ")
                    query = "SELECT * FROM TBL_USUARIOS WHERE Nascimento > TO_DATE(:1, 'YYYY-MM-DD')"
                    inst_cadastro.execute(query, [nascimento])
                elif tipo_filtro == '3':
                    nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ")
                    query = "SELECT * FROM TBL_USUARIOS WHERE Nascimento < TO_DATE(:1, 'YYYY-MM-DD')"
                    inst_cadastro.execute(query, [nascimento])
                elif tipo_filtro == '4':
                    nascimento_inicio = input("Digite a data de início (YYYY-MM-DD): ")
                    nascimento_fim = input("Digite a data de término (YYYY-MM-DD): ")
                    query = "SELECT * FROM TBL_USUARIOS WHERE Nascimento BETWEEN TO_DATE(:1, 'YYYY-MM-DD') AND TO_DATE(:2, 'YYYY-MM-DD')"
                    inst_cadastro.execute(query, [nascimento_inicio, nascimento_fim])
                else:
                    print("Opção inválida.")
                    return

            registros = inst_cadastro.fetchall()
            if not registros:
                print("\nNenhum registro encontrado.")
            else:
                for registro in registros:
                    print(registro)
            print("_" * 70)
            input("\nENTER para continuar...")
    except oracledb.DatabaseError as e:
        print(f"Erro ao filtrar registros: {e}")

# Programa principal
def programa_principal() -> None:
    conn = conectar_bd()
    if conn is None:
        return  # Se a conexão falhar, encerra o programa

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("0 - Sair")
        print("1 - Listar registros")
        print("2 - Adicionar registro")
        print("3 - Editar registro")
        print("4 - Desativar registro")
        print("5 - Análise dos Usuários Registrados") 
        print("6 - Filtrar registros")  # Nova opção para filtrar registros

        opcao = input("\nEscolha uma opção: ")

        if opcao == '0':
            break
        elif opcao == '1':
            listar_registros_opcao(conn)
        elif opcao == '2':
            adicionar_registro(conn)
        elif opcao == '3':
            id_registro = int(input("Digite o ID do registro a ser editado: "))
            editar_registro(conn, id_registro)
        elif opcao == '4':
            id_registro = int(input("Digite o ID do registro a ser desativado: "))
            excluir_registro_logico(conn, id_registro)
        elif opcao == '5':
            listar_registros_com_pandas(conn)
        elif opcao == '6':  # Chama a nova função de filtro
            filtrar_registros(conn)
        else:
            print("Opção inválida.")

        continuar = input("\nDeseja realizar outra operação? (S/N): ").lower()
        if continuar != 's':
            break

    conn.close()
    print("Conexão fechada.")


# Execução do Programa
programa_principal()