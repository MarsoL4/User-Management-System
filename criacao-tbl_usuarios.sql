CREATE TABLE TBL_USUARIOS (
    ID NUMBER(38, 0) GENERATED ALWAYS AS IDENTITY,  -- ID gerado automaticamente
    NOME VARCHAR2(100 BYTE),                        -- Nome do usu�rio
    IDADE NUMBER,                                   -- Idade do usu�rio
    CIDADE VARCHAR2(100 BYTE),                      -- Cidade do usu�rio
    PROFISSAO VARCHAR2(100 BYTE),                   -- Profiss�o do usu�rio
    ATIVO NUMBER(1, 0) DEFAULT 1,                   -- Indica se o usu�rio est� ativo (1) ou desativado (0)
    SALARIO NUMBER(10, 2),                          -- Sal�rio do usu�rio
    NASCIMENTO DATE,                                -- Data de nascimento do usu�rio
    CONSTRAINT PK_USUARIOS PRIMARY KEY (ID)         -- Definindo a chave prim�ria
);