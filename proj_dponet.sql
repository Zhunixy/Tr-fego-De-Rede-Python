-- Criar o banco de dados "proj_dponet"
create database if not exists `proj_dponet`;

-- Usar o banco de dados "proj_dponet"
use `proj_dponet`;

-- Criar a tabela "user" dentro do banco de dados "proj_dponet"
create table if not exists `proj_dponet`.`user` (
`id` int auto_increment, -- Atributo "id", tipo inteiro, preenchimento automático
`name` varchar(45) not null, -- Atributo "name", tipo texto, 45 caracteres, não pode ser vazio
`cpf_cnpj` varchar(45) not null unique, -- Atributo "ident", tipo texto, 45 caracteres, não pode ser vazio, unico
`telefone` varchar(45) not null unique, -- Atributo "telefone", tipo texto, 45 caracteres, não pode ser vazio, unico
`email` varchar(45) not null unique, -- Atributo "email", tipo texto, 45 caracteres, não pode ser vazio, unico
`password` varchar(100) not null, -- Atributo "password", tipo texto, 100 caracteres, não pode ser vazio
primary key (`id`) -- Declaração da chave primária
);

-- Criar a tabela "history" dentro do banco de dados "proj_dponet"
create table if not exists `proj_dponet`.`history` (
`id` int auto_increment, -- Atributo "id", tipo inteiro, preenchimento automático
`date`date not null, -- Atributo "date", tipo data, não pode ser vazio
`description` varchar(45) not null, -- Atributo "description", tipo texto, 45 caracteres, não pode ser vazio
`document` varchar(45) not null unique, -- Atributo "document", tipo texto, 45 caracteres, não pode ser vazio, unico
`user_id` int not null, -- Atributo "user_id", tipo inteiro, não pode ser vazio
primary key (`id`), -- Declaração da chave primária
foreign key (`user_id`) references `user`(`id`) -- Declaração de chave estrangeira
);

INSERT INTO `USER` VALUEs (NULL, 'Teste', 99999999999, 99999999999, 'teste@teste', 'teste');
