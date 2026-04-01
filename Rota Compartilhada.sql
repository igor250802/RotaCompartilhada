-- Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS rota_compartilhada;
USE rota_compartilhada;

-- 1. Tabela de Usuários (RF01, RF02)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario)
) ENGINE=InnoDB;

-- 2. Tabela de Veículos (Complemento ao RF03)
CREATE TABLE IF NOT EXISTS veiculos (
    id_veiculo INT NOT NULL AUTO_INCREMENT,
    id_proprietario INT NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    placa VARCHAR(10) NOT NULL UNIQUE,
    cor VARCHAR(30),
    ano INT NOT NULL, 
    PRIMARY KEY (id_veiculo),
    CONSTRAINT fk_veiculo_usuario 
        FOREIGN KEY (id_proprietario) 
        REFERENCES usuarios(id_usuario) 
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. Tabela de Viagens (RF03)
CREATE TABLE IF NOT EXISTS viagens (
    id_viagem INT NOT NULL AUTO_INCREMENT,
    id_motorista INT NOT NULL,
    id_veiculo INT NOT NULL,
    data_hora DATETIME NOT NULL,
    vagas_totais INT NOT NULL,
    status_viagem ENUM('Aberta', 'Em Curso', 'Finalizada', 'Cancelada') DEFAULT 'Aberta',
    PRIMARY KEY (id_viagem),
    CONSTRAINT fk_viagem_motorista 
        FOREIGN KEY (id_motorista) 
        REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_viagem_veiculo 
        FOREIGN KEY (id_veiculo) 
        REFERENCES veiculos(id_veiculo)
) ENGINE=InnoDB;

-- 4. Tabela de Paradas (Itinerário)
CREATE TABLE IF NOT EXISTS paradas (
    id_parada INT NOT NULL AUTO_INCREMENT,
    id_viagem INT NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    ordem_parada INT NOT NULL, -- Ex: 1=Muzambinho, 2=Guaxupé...
    PRIMARY KEY (id_parada),
    CONSTRAINT fk_parada_viagem 
        FOREIGN KEY (id_viagem) 
        REFERENCES viagens(id_viagem) 
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5. Tabela de Reservas (RF04, RF06, RF07)
CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INT NOT NULL AUTO_INCREMENT,
    id_viagem INT NOT NULL,
    id_passageiro INT NOT NULL,
    id_parada_embarque INT NOT NULL,
    id_parada_desembarque INT NOT NULL,
    quantidade_bagagem INT NOT NULL DEFAULT 0,
    status_solicitacao ENUM('Pendente', 'Aceita', 'Recusada') DEFAULT 'Pendente',
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_reserva),
    CONSTRAINT fk_reserva_viagem 
        FOREIGN KEY (id_viagem) 
        REFERENCES viagens(id_viagem) 
        ON DELETE CASCADE,
    CONSTRAINT fk_reserva_passageiro 
        FOREIGN KEY (id_passageiro) 
        REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_reserva_embarque 
        FOREIGN KEY (id_parada_embarque) 
        REFERENCES paradas(id_parada),
    CONSTRAINT fk_reserva_desembarque 
        FOREIGN KEY (id_parada_desembarque) 
        REFERENCES paradas(id_parada)
) ENGINE=InnoDB;