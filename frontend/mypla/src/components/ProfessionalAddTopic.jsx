import { getTopics } from '../services/topics/topics.service';
import {
  getProfessionalTopics,
  postProfessionalTopics,
  deleteProfessionalTopics,
  putProfesionalTopics,
} from '../services/professionals-topic/professionals-topic.service.js';

import React, { useEffect, useState } from 'react';
import { Button, Box, Typography } from '@mui/material';
import ScheduleTopics from './shedule/schedule-components/ScheduleTopics';
import ScheduleTopicsReservation from './reservation/ScheduleTopicsReservation.jsx';
import ScheduleTopicsProfile from './profile/ScheduleTopicsProfile.jsx';
import InputPrice from './profile/InputPrice.jsx';
import ModalProfile from './profile/ModalProfile.jsx';

export default function ProfessionalAddTopic({ token }) {
  const [allTopics, setAllTopics] = useState([]);
  const [initialTopics, setInitialTopics] = useState([]);
  const [notSelectedTopics, setNotSelectedTopics] = useState([]);
  const [selectTopic, setSelectTopic] = useState([]);
  const [clickTopic, setClickTopic] = useState({});
  const [openModal, setOpenModal] = useState(false)
  const [price, setPrice] = useState(0)
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const fetchTopicsData = async () => {
    try {
      setLoading(true);
      const { data: all, error: allError } = await getTopics();
      const assigned = await getProfessionalTopics(token, true);

      if (allError) {
        console.error('Error obteniendo tópicos:', allError);
        setStatusMessage('Error al obtener los tópicos');
        return;
      }

      console.log (all.filter(a => assigned.find(s => s.topic_name !== a)), "FILTER")
      setAllTopics(all || []);
      setInitialTopics(assigned || []);
      setNotSelectedTopics(all.filter(a => !assigned.find(s => s.topic_name === a)) || []);
      setPrice(0)
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
    console.log(data, "DATA")
    setSelectTopic(data)
  };

  const handleConfirmChanges = async () => {
    try {
      setLoading(true);
      setStatusMessage('');

      const { error } = await postProfessionalTopics(token, selectTopic, price)
      if (error) {
        console.error(`Error al agregar el tópico ${topic}:`, error);
        setStatusMessage(`Error al agregar el tópico ${topic}`);
        return;
      }
      await fetchTopicsData()
    } catch (error) {
      console.error('Error al aplicar cambios:', error);
      setStatusMessage('Error al aplicar cambios');
    } finally {
      setLoading(false);
    }
    /*
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
  };*/
  }

  const handleUpdatePrice = async (topic) => {
    try {
      const { error } = await putProfesionalTopics(token, topic)
      if (error) {
        console.error(error)
      }
      setOpenModal(false)
      await fetchTopicsData()
    } catch (err) {
      console.error(err)
    }
  }

  const handleDeleteTopic = async () => {
    try {
      const { error } = await deleteProfessionalTopics(token, clickTopic.topic_name)
      if (error) {
        console.error(error)
      }
      setOpenModal(false)
      await fetchTopicsData()
    } catch (err) {
      console.error(err)
    }
  }

  const handleOpenModal = (topic) => {
    setClickTopic(topic)
    setOpenModal(true)
  }

  return (
    <Box>
      <Typography variant="h6">Editá tus tópicos:</Typography>

      {loading && <Typography>Cargando...</Typography>}

      {!loading && (
        <>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {initialTopics.map((topic) => (
              <div
                key={topic.topic_name}
                onClick={() => handleOpenModal(topic)}
                style={{
                  backgroundColor: '#1cb698',
                  color: '#fff',
                  padding: '6px 12px',
                  borderRadius: '20px',
                  fontSize: '0.9rem',
                  cursor: 'pointer'
                }}
              >
                {topic.topic_name + " $" + topic.price_class}
              </div>
            ))}
          </div>
          {notSelectedTopics.length > 0 ? <div> <ScheduleTopicsProfile
            isEditable={false}
            onChange={handleChangeTopics}
            value={selectTopic}
            topicsList={notSelectedTopics}
          />

          <InputPrice 
            value={price} 
            onChange={(newPrice) => setPrice(newPrice)} 
            label="Precio del servicio"
            currencySymbol="$"
          />

          <Button
            variant="contained"
            color="primary"
            onClick={handleConfirmChanges}
            sx={{ marginTop: 2 }}
          >
            Agregar tópico
          </Button> </div> : <p>Ya tiene todo los tópicos asignados</p>}
          

          <ModalProfile
            open={openModal}
            onClose={() => setOpenModal(false)}
            topic={clickTopic?.topic_name}
            currentPrice={clickTopic?.price_class}
            onSave={handleUpdatePrice}
            onDelete={handleDeleteTopic}
          />
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
