-- Crear tabla de eventos

CREATE TABLE IF NOT EXISTS profesional (
    user_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE evento (
    event_timestamp TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    PRIMARY KEY (event_timestamp, user_id),
    CONSTRAINT fk_profesional FOREIGN KEY (user_id) REFERENCES profesional(user_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION validar_ranura_horaria()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM evento 
        WHERE user_id = NEW.user_id 
        AND event_timestamp >= date_trunc('hour', NEW.event_timestamp) 
        AND event_timestamp < date_trunc('hour', NEW.event_timestamp) + INTERVAL '1 hour'
    ) THEN
        RAISE EXCEPTION 'Ya existe un evento en la misma ranura horaria para este profesor';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

INSERT INTO profesional (user_id, nombre) VALUES (1, 'Carlos');
INSERT INTO profesional (user_id, nombre) VALUES (2, 'Pepe');
INSERT INTO profesional (user_id, nombre) VALUES (3, 'Maria');

-- Insertar datos iniciales
INSERT INTO evento (user_id, titulo, descripcion, event_timestamp) VALUES
(1, 'Capacitacion en Capacitores', 'Como lidiar con patadas electricas y manejo de aislamiento', 
    '2025-04-01 10:00:00');
INSERT INTO evento (user_id, titulo, descripcion, event_timestamp) VALUES
(1, '30 Formas de cocinar pollo', 'Breve introducion al arte de cocinar pollo', 
    '2025-04-05 15:00:00');
INSERT INTO evento (user_id, titulo, descripcion, event_timestamp) VALUES
(2, 'Como enseñarle a tu perro a hablar en 15 idiomas', 'Ademas de escribir', 
    '2025-04-05 15:00:00');
INSERT INTO evento (user_id, titulo, descripcion, event_timestamp) VALUES
(2, 'Como organizar un cumpleaños sorpresa', 'Introduccion a la dinamica social epistemologica', 
    '2025-04-05 16:30:00');

CREATE OR REPLACE FUNCTION get_eventos_profesional(id_profesional_input INTEGER)
RETURNS TABLE (
  nombre_profesional VARCHAR(255),
  timestamp_evento TIMESTAMP,
  titulo_evento VARCHAR(255),
  descripcion_evento TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    p.nombre,
    e.event_timestamp,
    e.titulo,
    e.descripcion
  FROM
    profesional p
  JOIN
    evento e ON p.user_id = e.user_id
  WHERE
    p.user_id = id_profesional_input;
END;
$$ LANGUAGE plpgsql;
