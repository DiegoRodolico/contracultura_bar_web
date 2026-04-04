-- ============================================
-- BASE DE DATOS: CONTRACULTURA_BAR
-- ============================================

-- 1. CREAR LA BASE DE DATOS (si no existe)
CREATE DATABASE IF NOT EXISTS contracultura_bar;

-- 2. USAR BASE DE DATOS
USE contracultura_bar;

-- ============================================
-- TABLA 1: CATEGORIAS 
-- Para organizar 
-- ============================================
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,           -- Número único que aumenta solo
    nombre VARCHAR(50) UNIQUE NOT NULL,          -- Nombre de la categoría (único)
    descripcion TEXT,                            -- Descripción opcional
    icono VARCHAR(20) DEFAULT '🍺'               -- Emoji para identificar
);

-- ============================================
-- TABLA 2: PRODUCTOS 
-- Lo que vendemos en el bar
-- ============================================
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,          	 -- ID único
    nombre VARCHAR(100) NOT NULL,               	 -- Nombre del producto
    categoria_id INT,                           	 -- A qué categoría pertenece
    precio DECIMAL(10, 2) NOT NULL,             	 -- Precio de venta
    costo DECIMAL(10, 2) NOT NULL,              	 -- Costo para vos 
    stock INT DEFAULT 0,                       		 -- Cuántos tenés
     stock_minimo INT DEFAULT 5,                 	 -- Alerta cuando baje a este número
    descripcion TEXT,                           	 -- Descripción para clientes
     activo BOOLEAN DEFAULT TRUE,                	 -- Si se muestra o no
     fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,	 -- Fecha automática
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) -- Relación con categorias
);

-- ============================================
-- TABLA 3: CLIENTES 
-- Para fidelizar clientes
-- ============================================
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,			-- ID unico
    nombre VARCHAR(100) NOT NULL,			-- Nombre del cliente
    telefono VARCHAR(20),				-- Telefono del cliente					
    puntos INT DEFAULT 0,				-- Puntos P/ Premios
--     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP	-- Fecha de Registro
);

-- ============================================
-- TABLA 4: MESAS 
-- Control de mesas del bar
-- ============================================
CREATE TABLE mesas (
    id INT PRIMARY KEY AUTO_INCREMENT,		 			-- ID unico 
    numero INT UNIQUE NOT NULL,                  			-- Número de mesa 
    capacidad INT DEFAULT 4,                     			-- Cuántas personas caben
    ubicacion ENUM('INTERIOR', 'AFUERA', 'BARRA', 'EXTERIOR', 'SILLON') DEFAULT 'INTERIOR',	-- Ubicacion de las mesas
     estado ENUM('LIBRE', 'OCUPADA', 'RESERVADA') DEFAULT 'LIBRE'	-- Estado de la mesa
);

-- ============================================
-- TABLA 5: PEDIDOS 
-- Cada vez que alguien pide algo
-- ============================================
CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,		 	-- ID unico
    mesa_id INT,                                 	-- En qué mesa se pidió
    cliente_id INT NULL,                         	-- Cliente (si es conocido)
    estado ENUM('PENDIENTE', 'EN_PROCESO', 'LISTO', 'ENTREGADO', 'CANCELADO') DEFAULT 'PENDIENTE',
    tipo ENUM('MESA', 'BARRA', 'PARA_LLEVAR') DEFAULT 'MESA',
    total DECIMAL(10, 2) DEFAULT 0,              	-- Total a pagar
    observaciones TEXT,                          	-- Pedidos especiales del pedido
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,	-- Fecha de creacion del pedido
    fecha_cierre TIMESTAMP NULL,                 	-- Cuando se paga
    FOREIGN KEY (mesa_id) REFERENCES mesas(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- ============================================
-- TABLA 6: DETALLE_PEDIDO 
-- Qué productos tiene cada pedido
-- ============================================
CREATE TABLE detalle_pedido (
    id INT PRIMARY KEY AUTO_INCREMENT,		 -- ID unico
    pedido_id INT,                               -- A qué pedido pertenece
    producto_id INT,                             -- Qué producto
    cantidad INT NOT NULL,                       -- Cuántos pidió
    precio_unitario DECIMAL(10, 2) NOT NULL,     -- Precio en ese momento
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED, -- Calcula solo
    estado ENUM('PENDIENTE', 'PREPARANDO', 'LISTO') DEFAULT 'PENDIENTE',
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE, -- Si borro pedido, borro esto
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
