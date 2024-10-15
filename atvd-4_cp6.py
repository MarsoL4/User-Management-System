# Imports ----------------------------
import os
import oracledb
import pandas as pd
import matplotlib.pyplot as plt

# Subalgoritmos ----------------------
# Cria conexão com o banco de dados
def conectar_bd() -> oracledb.Connection:
    try:
        conn = oracledb.connect(conn = oracledb.connect(user="SEU_USUARIO", password="SUA_SENHA", dsn="SEU_HOST_NAME:SUA_PORTA/SEU_SID")
)
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
        with conn.cursor() as inst_cadastro:
            cadastro = """
            INSERT INTO TBL_USUARIOS (ID, Nome, Idade, Cidade, Profissao) 
            VALUES (:1, :2, :3, :4, :5)"""
            inst_cadastro.execute(cadastro, [novo_id, nome, idade, cidade, profissao])
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

    if updates:
        try:
            with conn.cursor() as inst_cadastro:
                editar = f"UPDATE TBL_USUARIOS SET {', '.join(updates)} WHERE ID = :5"
                inst_cadastro.execute(editar, valores + [id_atual])
                conn.commit()
                print("\nRegistro atualizado com sucesso!")
                print("-" * 70)
        except oracledb.DatabaseError as e:
            print(f"Erro ao atualizar registro: {e}")

# Exclui um registro
def excluir_registro(conn: oracledb.Connection, id_atual: int) -> None:
    try:
        with conn.cursor() as inst_cadastro:
            excluir = "DELETE FROM TBL_USUARIOS WHERE ID = :1"
            inst_cadastro.execute(excluir, [id_atual])
            conn.commit()
            print("\nRegistro excluído com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao excluir registro: {e}")

# Função para listar todos os registros
def listar_registros(conn: oracledb.Connection) -> None:
    try:
        with conn.cursor() as inst_cadastro:
            inst_cadastro.execute("SELECT * FROM TBL_USUARIOS")
            registros = inst_cadastro.fetchall()

            if not registros:
                print("\nNenhum registro cadastrado.")
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

            if not registros:
                print("\nNenhum registro cadastrado.")
            else:
                df = pd.DataFrame(registros, columns=['ID', 'Nome', 'Idade', 'Cidade', 'Profissao'])
                print(df)
                print("_" * 70)

                # Exibe média de idades e mostra gráfico
                media_idade = df['Idade'].mean()
                print(f"\nMédia de idade dos usuários: {media_idade:.2f}")
                df['Idade'].plot(kind='hist', title="Distribuição de Idades", color='blue')
                plt.xlabel('Idade')
                plt.ylabel('Frequência')
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
    print("_" * 70)

# Programa principal que executa as operações
def programa_principal() -> None:
    conn = conectar_bd()
    if conn is None:
        return  # Se a conexão falhar, encerra o programa

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        pk = input("Digite a chave primária (ID), 'L' para listar registros, 'A' para análise de dados ou 0 para sair: ")

        if pk.lower() == 'l':
            listar_registros(conn)
        elif pk.lower() == 'a':
            listar_registros_com_pandas(conn)
        elif pk == '0':
            break
        else:
            try:
                pk = int(pk)
                with conn.cursor() as inst_cadastro:
                    inst_cadastro.execute("SELECT * FROM TBL_USUARIOS WHERE ID = :1", [pk])
                    registro = inst_cadastro.fetchone()

                    if registro:
                        exibir_detalhes_registro(registro)

                        while True:
                            opcao = input("\nDeseja Editar (E), Excluir (X), ou Sair (0)? ").lower()
                            if opcao == 'e':
                                editar_registro(conn, pk)
                                break
                            elif opcao == 'x':
                                excluir_registro(conn, pk)
                                break
                            elif opcao == '0':
                                break
                            else:
                                print("Opção inválida.")
                    else:
                        print("\nRegistro não encontrado. Vamos cadastrar um novo.")
                        adicionar_registro(conn)
            except ValueError:
                print("ID inválido. Deve ser um número.")
            except oracledb.DatabaseError as e:
                print(f"Erro ao consultar registro: {e}")

        continuar = input("\nDeseja realizar outra operação? (S/N): ").lower()
        if continuar != 's':
            break

    conn.close()
    print("Conexão fechada.")

# Execução do Programa
programa_principal()
