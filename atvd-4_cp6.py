# Imports ----------------------------
import os
import oracledb
import pandas as pd
import matplotlib.pyplot as plt

# Subalgoritmos ----------------------
# Cria conexão com o banco de dados
def conectar_bd() -> oracledb.Connection:
    try:
        conn = oracledb.connect(user="RM556310", password="130206", dsn="oracle.fiap.com.br:1521/ORCL")
        print("Conexão aberta com sucesso!")
        return conn
    except oracledb.DatabaseError as e:
        print(f"Erro de conexão: {e}")
        return None

# Adiciona novo registro no banco de dados (agora inclui o campo ATIVO)
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
            INSERT INTO TBL_USUARIOS (ID, Nome, Idade, Cidade, Profissao, ATIVO) 
            VALUES (:1, :2, :3, :4, :5, :6)"""
            inst_cadastro.execute(cadastro, [novo_id, nome, idade, cidade, profissao, True])
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
        query = "SELECT ID, Nome, Idade, Cidade, Profissao, ATIVO FROM TBL_USUARIOS"
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
            df = pd.DataFrame(registros, columns=['ID', 'Nome', 'Idade', 'Cidade', 'Profissao', 'ATIVO'])

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
    print(f"ATIVO: {registro[5]}")
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
            tipo_listagem = input("Listar (A)tivados, (D)esativados ou (T)odos? ").lower()
            if tipo_listagem == 'a':
                listar_registros(conn, True)
            elif tipo_listagem == 'd':
                listar_registros(conn, False)
            else:
                listar_registros(conn)
        elif pk.lower() == 'a':
            listar_registros_com_pandas(conn)
        elif pk == '0':
            break
        else:
            try:
                pk = int(pk)
                with conn.cursor() as inst_cadastro:
                    inst_cadastro.execute("SELECT ID, Nome, Idade, Cidade, Profissao, ATIVO FROM TBL_USUARIOS WHERE ID = :1", [pk])
                    registro = inst_cadastro.fetchone()

                    if registro:
                        exibir_detalhes_registro(registro)

                        while True:
                            opcao = input("\nDeseja Editar (E), Desativar (X), ou Sair (0)? ").lower()
                            if opcao == 'e':
                                editar_registro(conn, pk)
                                break
                            elif opcao == 'x':
                                excluir_registro_logico(conn, pk)
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
