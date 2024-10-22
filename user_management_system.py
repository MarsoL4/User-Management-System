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

# Adiciona novo registro no banco de dados
def adicionar_registro(conn: oracledb.Connection) -> None:
    print("-" * 70)
    
    try:
        novo_id = int(input("\nDigite o ID (PK): "))
    except ValueError:
        print("ID inválido. Deve ser um número.")
        return
    
    nome = input("\nDigite o nome: ")
    
    try:
        idade = int(input("\nDigite a idade: "))
    except ValueError:
        print("Idade inválida. Deve ser um número.")
        return
    
    cidade = input("\nDigite a cidade: ")
    profissao = input("\nDigite a profissão: ")

    try:
        salario = float(input("\nDigite o salário: "))
    except ValueError:
        print("Salário inválido. Deve ser um número.")
        return
    
    nascimento = input("\nDigite a data de nascimento (YYYY-MM-DD): ")

    try:
        with conn.cursor() as inst_cadastro:
            cadastro = """
            INSERT INTO TBL_USUARIOS (ID, Nome, Idade, Cidade, Profissao, Salario, Nascimento, ATIVO) 
            VALUES (:1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'), :8)"""
            inst_cadastro.execute(cadastro, [novo_id, nome, idade, cidade, profissao, salario, nascimento, True])
            conn.commit()
            print("\nDados inseridos na tabela com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao inserir dados: {e}")

# Edita um registro existente
def editar_registro(conn: oracledb.Connection, id_atual: int) -> None:
    print("Digite os novos valores ou pressione Enter para manter os antigos.")
    
    novo_nome = input(f"\nNome atual: ") or None
    nova_idade = input(f"\nIdade atual: ")
    nova_cidade = input(f"\nCidade atual: ") or None
    nova_profissao = input(f"\nProfissão atual: ") or None
    novo_salario = input(f"\nSalário atual: ") or None
    novo_nascimento = input(f"\nNascimento atual (YYYY-MM-DD): ") or None

    updates = []
    valores = []
    
    if novo_nome:
        updates.append("Nome = :1")
        valores.append(novo_nome)
    if nova_idade:
        try:
            nova_idade = int(nova_idade)
            updates.append("Idade = :2")
            valores.append(nova_idade)
        except ValueError:
            print("Idade inválida. Deve ser um número.")
            return
    if nova_cidade:
        updates.append("Cidade = :3")
        valores.append(nova_cidade)
    if nova_profissao:
        updates.append("Profissao = :4")
        valores.append(nova_profissao)
    if novo_salario:
        try:
            novo_salario = float(novo_salario)
            updates.append("Salario = :5")
            valores.append(novo_salario)
        except ValueError:
            print("Salário inválido. Deve ser um número.")
            return
    if novo_nascimento:
        updates.append("Nascimento = TO_DATE(:6, 'YYYY-MM-DD')")
        valores.append(novo_nascimento)

    if updates:
        try:
            with conn.cursor() as inst_cadastro:
                editar = f"UPDATE TBL_USUARIOS SET {', '.join(updates)} WHERE ID = :7"
                inst_cadastro.execute(editar, valores + [id_atual])
                conn.commit()
                print("\nRegistro atualizado com sucesso!")
                print("-" * 70)
        except oracledb.DatabaseError as e:
            print(f"Erro ao atualizar registro: {e}")

# Simula a exclusão de um registro (exclusão lógica: ATIVO = False)
def excluir_registro_logico(conn: oracledb.Connection, id_atual: int) -> None:
    try:
        with conn.cursor() as inst_cadastro:
            excluir = "UPDATE TBL_USUARIOS SET ATIVO = :1 WHERE ID = :2"
            inst_cadastro.execute(excluir, [False, id_atual])
            conn.commit()
            print("\nRegistro desativado (exclusão lógica) com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao desativar registro: {e}")

# Função para listar registros (ativados, desativados ou todos)
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
        with conn.cursor() as inst_cadastro:
            inst_cadastro.execute("SELECT * FROM TBL_USUARIOS")
            registros = inst_cadastro.fetchall()
            
            # Criar DataFrame com a coluna 'ATIVO'
            df = pd.DataFrame(registros, columns=['ID', 'Nome', 'Idade', 'Cidade', 'Profissao', 'Salario', 'Nascimento', 'ATIVO'])

            # Exibir o DataFrame
            print(df)
            print("_" * 70)

            # Calcular e exibir a média de idade
            if not df.empty:
                media_idade = df['Idade'].mean()
                print(f"Média de Idade: {media_idade:.2f}")
                print(f"Número de Registros: {len(df)}")
                
                # Plotar gráfico de idades
                plt.figure(figsize=(10, 6))
                plt.bar(df['Nome'], df['Idade'], color='skyblue')
                plt.axhline(y=media_idade, color='r', linestyle='--', label=f'Média de Idade: {media_idade:.2f}')
                plt.title('Idade dos Usuários')
                plt.xlabel('Nome')
                plt.ylabel('Idade')
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                plt.show()

            input("\nENTER para continuar...")
    except oracledb.DatabaseError as e:
        print(f"Erro ao listar registros: {e}")

# Função para exibir detalhes de um registro
def exibir_detalhes_registro(registro) -> None:
    print("\nDetalhes do Registro:")
    print(f"ID: {registro[0]}")
    print(f"Nome: {registro[1]}")
    print(f"Idade: {registro[2]}")
    print(f"Cidade: {registro[3]}")
    print(f"Profissão: {registro[4]}")
    print(f"Salário: {registro[5]}")
    print(f"Nascimento: {registro[6]}")
    print(f"ATIVO: {registro[7]}")
    print("_" * 70)

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
                    nascimento_min = input("Digite a data inicial (YYYY-MM-DD): ")
                    nascimento_max = input("Digite a data final (YYYY-MM-DD): ")
                    query = "SELECT * FROM TBL_USUARIOS WHERE Nascimento BETWEEN TO_DATE(:1, 'YYYY-MM-DD') AND TO_DATE(:2, 'YYYY-MM-DD')"
                    inst_cadastro.execute(query, [nascimento_min, nascimento_max])
                else:
                    print("Opção inválida.")
                    return
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

# Programa principal atualizado
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
        print("5 - Filtrar registros")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '0':
            break
        elif opcao == '1':
            listar_registros(conn)
        elif opcao == '2':
            adicionar_registro(conn)
        elif opcao == '3':
            id_registro = int(input("Digite o ID do registro a ser editado: "))
            editar_registro(conn, id_registro)
        elif opcao == '4':
            id_registro = int(input("Digite o ID do registro a ser desativado: "))
            excluir_registro_logico(conn, id_registro)
        elif opcao == '5':
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
