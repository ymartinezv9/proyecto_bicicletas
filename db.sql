CREATE DATABASE bicicletas_db;
USE bicicletas_db;

USE bicicletas_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    cui VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(15),
    contrasena VARCHAR(255) NOT NULL,
    tipo ENUM('Usuario', 'Administrador', 'Tecnico', 'Soporte') DEFAULT 'Usuario',
    estado ENUM('Activo', 'Bloqueado') DEFAULT 'Activo',
    intentos_fallidos INT DEFAULT 0
);

SHOW TABLES;
ALTER TABLE usuarios MODIFY contrasena BLOB NOT NULL;

USE bicicletas_db;

CREATE TABLE terminales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(255),
    capacidad INT,
    ocupadas INT DEFAULT 0
);

CREATE TABLE bicicletas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE,
    estado ENUM('Disponible', 'En Uso', 'Mantenimiento') DEFAULT 'Disponible',
    terminal_id INT,
    FOREIGN KEY (terminal_id) REFERENCES terminales(id)
);

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    bicicleta_id INT,
    terminal_origen_id INT,
    terminal_destino_id INT,
    pin VARCHAR(6),
    estado ENUM('Activa', 'Completada', 'Cancelada') DEFAULT 'Activa',
    fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (bicicleta_id) REFERENCES bicicletas(id),
    FOREIGN KEY (terminal_origen_id) REFERENCES terminales(id),
    FOREIGN KEY (terminal_destino_id) REFERENCES terminales(id)
);

USE bicicletas_db;

INSERT INTO terminales (nombre, ubicacion, capacidad, ocupadas)
VALUES
('Terminal Central', 'Zona 1, Ciudad', 10, 2),
('Terminal Norte', 'Zona 18, Ciudad', 8, 3),
('Terminal Sur', 'Zona 12, Ciudad', 6, 1);

USE bicicletas_db;

INSERT INTO bicicletas (codigo, estado, terminal_id) VALUES
('BIKE001', 'Disponible', 1),
('BIKE002', 'Disponible', 1),
('BIKE003', 'En Uso', 1),
('BIKE004', 'Disponible', 2),
('BIKE005', 'Mantenimiento', 2),
('BIKE006', 'Disponible', 3);



SELECT id, nombre, correo FROM usuarios;

SELECT * FROM terminales;
SELECT * FROM bicicletas;
SELECT * FROM usuarios;

CREATE TABLE reportes_problemas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    bicicleta_id INT,
    tipo_problema VARCHAR(100),
    descripcion TEXT,
    estado ENUM('Pendiente', 'Revisado', 'Resuelto') DEFAULT 'Pendiente',
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (bicicleta_id) REFERENCES bicicletas(id)
);

CREATE TABLE mensajes_soporte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    asunto VARCHAR(100),
    mensaje TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente', 'Atendido') DEFAULT 'Pendiente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE preferencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE,
    notificaciones BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE rutas_favoritas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    terminal_origen_id INT,
    terminal_destino_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (terminal_origen_id) REFERENCES terminales(id),
    FOREIGN KEY (terminal_destino_id) REFERENCES terminales(id)
);

ALTER TABLE reservas
ADD COLUMN hora_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN hora_fin DATETIME DEFAULT NULL;

SET SQL_SAFE_UPDATES = 0;

USE bicicletas_db;
UPDATE reservas SET hora_inicio = NOW() - INTERVAL 45 MINUTE WHERE estado = 'Activa';

ALTER TABLE bicicletas
ADD COLUMN latitud DECIMAL(10, 6) DEFAULT NULL,
ADD COLUMN longitud DECIMAL(10, 6) DEFAULT NULL;

UPDATE bicicletas SET latitud = 14.6349, longitud = -90.5069 WHERE id = 1;
UPDATE bicicletas SET latitud = 14.6123, longitud = -90.5150 WHERE id = 2;
UPDATE bicicletas SET latitud = 14.5896, longitud = -90.4872 WHERE id = 3;

DESCRIBE usuarios;

