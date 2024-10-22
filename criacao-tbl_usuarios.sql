CREATE TABLE TBL_USUARIOS (
    ID NUMBER(38, 0) GENERATED ALWAYS AS IDENTITY,  -- ID gerado automaticamente
    NOME VARCHAR2(100 BYTE),                        -- Nome do usuário
    IDADE NUMBER,                                   -- Idade do usuário
    CIDADE VARCHAR2(100 BYTE),                      -- Cidade do usuário
    PROFISSAO VARCHAR2(100 BYTE),                   -- Profissão do usuário
    ATIVO NUMBER(1, 0) DEFAULT 1,                   -- Indica se o usuário está ativo (1) ou desativado (0)
    SALARIO NUMBER(10, 2),                          -- Salário do usuário
    NASCIMENTO DATE,                                -- Data de nascimento do usuário
    CONSTRAINT PK_USUARIOS PRIMARY KEY (ID)         -- Definindo a chave primária
);