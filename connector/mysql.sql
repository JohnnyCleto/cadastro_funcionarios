# Criar Database
CREATE DATABASE if not exists empresa;

# Usar Database
USE empresa;

/*
Criar tabelas
    Setor
    Cargo
	Funcionário
*/
CREATE TABLE setor(
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome VARCHAR(50) /* NOT NULL */
);

CREATE TABLE cargo(
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome VARCHAR(50) /* NOT NULL */,
    setor_id INT,
    FOREIGN KEY (setor_id) REFERENCES setor(id)
);

CREATE TABLE funcionário(
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome VARCHAR(50) NOT NULL,
    sobrenome VARCHAR(50) NOT NULL,
    data_de_admissão DATE NOT NULL,
    status_funcionário BOOL /* NOT NULL */,
    # cargo_id INT,
    setor_id INT,
    # FOREIGN KEY (cargo_id) REFERENCES cargo(id),
    FOREIGN KEY (setor_id) REFERENCES setor(id)
);

/*
ALTER
*/
ALTER TABLE empresa.setor MODIFY COLUMN nome VARCHAR(50) NOT NULL;
ALTER TABLE empresa.cargo MODIFY COLUMN nome VARCHAR(50) NOT NULL;
ALTER TABLE empresa.funcionário MODIFY COLUMN status_funcionário BOOL NOT NULL;
ALTER TABLE empresa.funcionário ADD COLUMN cargo_id INT;
ALTER TABLE empresa.funcionário ADD FOREIGN KEY (cargo_id) REFERENCES cargo(id);

/*
Consulta
*/
SELECT * FROM empresa.setor;
SELECT * FROM empresa.funcionário;