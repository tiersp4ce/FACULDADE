
CREATE TABLE Livros (
    id INT PRIMARY KEY AUTO_INCREMENT,
  	titulo VARCHAR(50) NOT NULL,
    autor VARCHAR(50) NOT NULL,
    genero VARCHAR(50) NOT NULL,
  	id_genero INT,
  	FOREIGN KEY (id_genero) REFERENCES genero(id)
);

Create Table genero(
	id INT PRIMARY KEY AUTO_INCREMENT, 
	nome VARCHAR(50)
);

CREATE TABLE Clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco VARCHAR(255) NOT NULL
);

CREATE TABLE Recepcionistas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  telefone INT NOT NULL,
  nome VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL,
  senha VARCHAR(45) NOT NULL,
);
  
CREATE TABLE Emprestimos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_livro INT NOT NULL,
    id_cliente INT NOT NULL,
	data_emprestimo DATE NOT NULL,
    data_devolucao DATE NOT NULL,
    FOREIGN KEY (id_livro) REFERENCES Livros(id_livro),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);


insert into livros (titulo, autor, genero) values ("Bela e a fera","Andre Feire","Fantasia"),("Aprendendo em Java","HitaloYo","Educação"),("Titanic","Leonardo de Caprio","Drama"),("Harry Potter: A pedra de loló","jk Rolling","Fantasia"),("Os amigos Covardes","Wallisson Gomes","Didatico"),;

insert into genero (nome) Values ("Terror"),("Educação"),("Drama"),("Fantasia"),("Didatico");
