import { getTopics } from '../services/topics/topics.service';
import { getProfessionalsTopic, postProfessionalsTopic } from '../services/professionals-topic/professionals-topic.service'

import React, { useEffect, useState } from 'react';
import { Button, Box, Typography } from '@mui/material';
import Topics from './schedule/scheduleInfo/Topics';


export default function ProfessionalAddTopic({token}) {
  const [availableTopics, setAvailableTopics] = useState([]);
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const fetchTopicsData = async () => {
    try {
      setLoading(true);

      const { data: allTopics, error: topicsError } = await getTopics();
      if (topicsError) {
        console.error('Error al obtener todos los tópicos:', topicsError);
        setStatusMessage('Error al obtener los tópicos');
        return;
      }

      const { data: professionalTopics, error: professionalError } = await getProfessionalsTopic(token);
      if (professionalError) {
        console.error('Error al obtener tópicos del profesional:', professionalError);
        setStatusMessage('Error al obtener los tópicos del profesional');
        return;
      }

      const topicsAlreadyAssigned = professionalTopics || [];
      const topicsToAdd = allTopics.filter((topic) => !topicsAlreadyAssigned.includes(topic));

      setAvailableTopics(topicsToAdd);
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
    setSelectedTopics(data.topics || []);
  };

  const handleAddTopics = async () => {
    if (!selectedTopics.length) {
      setStatusMessage('Selecciona al menos un tópico');
      return;
    }

    try {
      setLoading(true);
      setStatusMessage('');

      for (const topic of selectedTopics) {
        const { data, error } = await postProfessionalsTopic(token, topic);
        if (error) {
          console.error(`Error al agregar el tópico ${topic}:`, error);
          setStatusMessage(`Error al agregar el tópico ${topic}`);
          return;
        }
      }

      setStatusMessage('Tópicos agregados correctamente');
      setSelectedTopics([]);
      await fetchTopicsData(); // Recarga los datos para actualizar la lista de disponibles
    } catch (error) {
      console.error('Error al agregar tópicos:', error);
      setStatusMessage('Error al agregar tópicos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6">Agregar tópicos al profesional</Typography>

      {loading && <Typography>Cargando...</Typography>}

      {!loading && (
        <>
          {availableTopics.length === 0 ? (
            <Typography color="text.secondary" sx={{ marginTop: 2 }}>
              El profesional ya tiene todos los tópicos asignados.
            </Typography>
          ) : (
            <>
              <Topics
                taskData={{ topics: selectedTopics }}
                isEditable={true}
                onChangeData={handleChangeTopics}
                topicsListFromParent={availableTopics}
              />

              <Button
                variant="contained"
                color="primary"
                onClick={handleAddTopics}
                sx={{ marginTop: 2 }}
              >
                Agregar tópicos
              </Button>
            </>
          )}

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
