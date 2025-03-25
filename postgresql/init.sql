-- Crear tabla de eventos
CREATE TABLE IF NOT EXISTS eventos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha TIMESTAMP NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos iniciales
INSERT INTO eventos (titulo, descripcion, fecha) VALUES
('Reunión de equipo', 'Planificación semanal', '2025-04-01 10:00:00'),
('Entrega de proyecto', 'Enviar informe final', '2025-04-05 15:00:00');
