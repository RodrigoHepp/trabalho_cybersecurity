-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS cybersecurity;
USE cybersecurity;

-- Tabela de Permissões
CREATE TABLE permissoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permissoes_nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);

-- Tabela de Papéis (papeis)
CREATE TABLE papeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    papeis_nome VARCHAR(50) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);


-- Tabela de Associação entre Papéis e Permissões
CREATE TABLE papeis_permissoes (
	id INT auto_increment primary key,
    papeis_id INT NOT NULL,
    permissoes_id INT NOT NULL,
    FOREIGN KEY (papeis_id) REFERENCES papeis(id),
    FOREIGN KEY (permissoes_id) REFERENCES permissoes(id)
);
   
-- Tabela de Usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- A senha será armazenada com hash
    papeis_id INT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (papeis_id) REFERENCES papeis(id) ON DELETE SET NULL
);

-- Tabela de Tokens
CREATE TABLE tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuarios_id INT NOT NULL,
    token VARCHAR(500) NOT NULL,
    data_expiracao TIMESTAMP NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(id)
);

