# Enzo Giuseppe Marsola 556310
# Renan Dorneles Boucault 557820
# Cauan da Cruz Ferreira 558238

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

