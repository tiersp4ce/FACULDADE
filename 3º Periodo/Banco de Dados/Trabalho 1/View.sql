CREATE DATABASE aula_visaodedados;
USE aula_visaodedados;

CREATE TABLE cliente (
    id INT PRIMARY KEY,
    nome VARCHAR(50),
    email VARCHAR(50),
    cidade VARCHAR(50)
);

CREATE TABLE produto (
    id INT PRIMARY KEY,
    nome_produto VARCHAR(50),
    preco DECIMAL(10, 2),
    estoque INT
);

CREATE TABLE venda (
    id INT PRIMARY KEY,
    cliente_id INT,
    produto_id INT,
    quantidade INT,
    data_venda DATE,
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id),
    FOREIGN KEY (produto_id) REFERENCES produto(id)
);

INSERT INTO cliente (id, nome, email, cidade) VALUES
(1, 'João Silva', 'joao@email.com', 'São Paulo'),
(2, 'Maria Souza', 'maria@email.com', 'Rio de Janeiro'),
(3, 'Pedro Lima', 'pedro@email.com', 'Belo Horizonte'),
(4, 'Ana Costa', 'ana@email.com', 'Curitiba'),
(5, 'Lucas Fernandes', 'lucas@email.com', 'Porto Alegre'),
(6, 'Julia Martins', 'julia@email.com', 'Salvador'),
(7, 'Carlos Pereira', 'carlos@email.com', 'Brasília'),
(8, 'Fernanda Santos', 'fernanda@email.com', 'Recife'),
(9, 'Rafael Almeida', 'rafael@email.com', 'Fortaleza'),
(10, 'Bianca Oliveira', 'bianca@email.com', 'Manaus');

INSERT INTO produto (id, nome_produto, preco, estoque) VALUES
(1, 'Notebook', 2500.00, 50),
(2, 'Smartphone', 1500.00, 100),
(3, 'Tablet', 900.00, 80),
(4, 'Monitor', 700.00, 30),
(5, 'Teclado', 100.00, 200),
(6, 'Mouse', 50.00, 300),
(7, 'Impressora', 600.00, 20),
(8, 'Fone de Ouvido', 80.00, 150),
(9, 'HD Externo', 250.00, 60),
(10, 'Câmera', 1200.00, 40);

INSERT INTO venda (id, cliente_id, produto_id, quantidade, data_venda, valor_total) VALUES
(1, 1, 1, 1, '2024-01-05', 2500.00),
(2, 2, 2, 2, '2024-02-10', 3000.00),
(3, 3, 3, 1, '2024-03-15', 900.00),
(4, 4, 4, 2, '2024-04-20', 1400.00),
(5, 5, 5, 3, '2024-05-25', 300.00),
(6, 6, 6, 5, '2024-06-30', 250.00),
(7, 7, 7, 1, '2024-07-05', 600.00),
(8, 8, 8, 4, '2024-08-10', 320.00),
(9, 9, 9, 2, '2024-09-15', 500.00),
(10, 10, 10, 1, '2024-10-20', 1200.00);


#VIEWS SIMPLES
CREATE VIEW VisaoSimples AS 
SELECT * FROM cliente
WHERE cidade LIKE 'Brasília';

#VIEWS COMPLEXO
CREATE VIEW VisaoComplexa AS
SELECT cliente.id AS ID_CLIENTE, 
cliente.nome as NOME_CLIENTE,
produto.nome_produto AS NOME_PRODUTO, 
produto.estoque AS ESTOQUE, 
venda.data_venda AS DATA_DE_VENDA,
produto.preco AS PRECO_UNITARIO, 
venda.valor_total AS VALOR_TOTAL_VENDA FROM venda 
JOIN cliente ON cliente.id = venda.cliente_id
JOIN produto ON produto.id = venda.produto_id
WHERE venda.data_venda BETWEEN '2024-05-25' AND '2024-10-25';
