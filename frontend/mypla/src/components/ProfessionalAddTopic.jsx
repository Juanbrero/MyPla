import { getTopics } from '../services/topics/topics.service';
import {
  getProfessionalTopics,
  postProfessionalTopics,
  deleteProfessionalTopics,
} from '../services/professionals-topic/professionals-topic.service.js';

import React, { useEffect, useState } from 'react';
import { Button, Box, Typography } from '@mui/material';
import ScheduleTopics from './shedule/schedule-components/ScheduleTopics';

export default function ProfessionalAddTopic({ token }) {
  const [allTopics, setAllTopics] = useState([]);
  const [initialTopics, setInitialTopics] = useState([]);
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const fetchTopicsData = async () => {
    try {
      setLoading(true);
      const { data: all, error: allError } = await getTopics();
      const assigned = await getProfessionalTopics(token);

      if (allError) {
        console.error('Error obteniendo tópicos:', allError);
        setStatusMessage('Error al obtener los tópicos');
        return;
      }

      setAllTopics(all || []);
      setInitialTopics(assigned || []);
      setSelectedTopics(assigned || []);
      setStatusMessage('');
    } catch (error) {
      console.error('Error inesperado:', error);
      setStatusMessage('Error inesperado');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) fetchTopicsData();
  }, [token]);

  const handleChangeTopics = (data) => {
    setSelectedTopics(data);
  };

  const handleConfirmChanges = async () => {
    const addedTopics = selectedTopics.filter(t => !initialTopics.includes(t));
    const removedTopics = initialTopics.filter(t => !selectedTopics.includes(t));

    if (addedTopics.length === 0 && removedTopics.length === 0) {
      setStatusMessage('No se detectaron cambios');
      return;
    }

    try {
      setLoading(true);
      setStatusMessage('');

      // Agregar nuevos tópicos
      for (const topic of addedTopics) {
        const { error } = await postProfessionalTopics(token, topic);
        if (error) {
          console.error(`Error al agregar el tópico ${topic}:`, error);
          setStatusMessage(`Error al agregar el tópico ${topic}`);
          return;
        }
      }

      // Eliminar tópicos deseleccionados
      for (const topic of removedTopics) {
        const { error } = await deleteProfessionalTopics(token, topic);
        if (error) {
          console.error(`Error al eliminar el tópico ${topic}:`, error);
          setStatusMessage(`Error al eliminar el tópico ${topic}`);
          return;
        }
      }

      setStatusMessage('Cambios guardados correctamente');
      await fetchTopicsData(); // Recargar datos
    } catch (error) {
      console.error('Error al aplicar cambios:', error);
      setStatusMessage('Error al aplicar cambios');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6">Editá tus tópicos:</Typography>

      {loading && <Typography>Cargando...</Typography>}

      {!loading && (
        <>
          <ScheduleTopics
            value={selectedTopics}
            isEditable={true}
            onChange={handleChangeTopics}
            topicsList={allTopics}
          />

          <Button
            variant="contained"
            color="primary"
            onClick={handleConfirmChanges}
            sx={{ marginTop: 2 }}
          >
            Confirmar cambios
          </Button>

          {statusMessage && (
            <Typography color="secondary" sx={{ marginTop: 2 }}>
              {statusMessage}
            </Typography>
          )}
        </>
      )}
    </Box>
  );
}
