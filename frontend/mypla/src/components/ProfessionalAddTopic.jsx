// import { getTopics } from '../services/topics/topics.service';
// import {
//   getProfessionalTopics,
//   postProfessionalTopics,
//   deleteProfessionalTopics,
//   putProfesionalTopics,
// } from '../services/professionals-topic/professionals-topic.service.js';

// import React, { useEffect, useState } from 'react';
// import { Button, Box, Typography } from '@mui/material';
// import ScheduleTopics from './shedule/schedule-components/ScheduleTopics';
// import ScheduleTopicsReservation from './reservation/ScheduleTopicsReservation.jsx';
// import ScheduleTopicsProfile from './profile/ScheduleTopicsProfile.jsx';
// import InputPrice from './profile/InputPrice.jsx';
// import ModalProfile from './profile/ModalProfile.jsx';

// export default function ProfessionalAddTopic({ token }) {
//   const [allTopics, setAllTopics] = useState([]);
//   const [initialTopics, setInitialTopics] = useState([]);
//   const [notSelectedTopics, setNotSelectedTopics] = useState([]);
//   const [selectTopic, setSelectTopic] = useState([]);
//   const [clickTopic, setClickTopic] = useState({});
//   const [openModal, setOpenModal] = useState(false)
//   const [price, setPrice] = useState(0)
//   const [loading, setLoading] = useState(false);
//   const [statusMessage, setStatusMessage] = useState('');

//   const fetchTopicsData = async () => {
//     try {
//       setLoading(true);
//       const { data: all, error: allError } = await getTopics();
//       const assigned = await getProfessionalTopics(token, true);

//       if (allError) {
//         console.error('Error obteniendo tópicos:', allError);
//         setStatusMessage('Error al obtener los tópicos');
//         return;
//       }

//       console.log (all.filter(a => assigned.find(s => s.topic_name !== a)), "FILTER")
//       setAllTopics(all || []);
//       setInitialTopics(assigned || []);
//       setNotSelectedTopics(all.filter(a => !assigned.find(s => s.topic_name === a)) || []);
//       setPrice(0)
//       setStatusMessage('');
//     } catch (error) {
//       console.error('Error inesperado:', error);
//       setStatusMessage('Error inesperado');
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     if (token) fetchTopicsData();
//   }, [token]);

//   const handleChangeTopics = (data) => {
//     console.log(data, "DATA")
//     setSelectTopic(data)
//   };

//   const handleConfirmChanges = async () => {
//     try {
//       setLoading(true);
//       setStatusMessage('');

//       const { error } = await postProfessionalTopics(token, selectTopic, price)
//       if (error) {
//         console.error(`Error al agregar el tópico ${topic}:`, error);
//         setStatusMessage(`Error al agregar el tópico ${topic}`);
//         return;
//       }
//       await fetchTopicsData()
//     } catch (error) {
//       console.error('Error al aplicar cambios:', error);
//       setStatusMessage('Error al aplicar cambios');
//     } finally {
//       setLoading(false);
//     }

//   }

//   const handleUpdatePrice = async (topic) => {
//     try {
//       const { error } = await putProfesionalTopics(token, topic)
//       if (error) {
//         console.error(error)
//       }
//       setOpenModal(false)
//       await fetchTopicsData()
//     } catch (err) {
//       console.error(err)
//     }
//   }

//   const handleDeleteTopic = async () => {
//     try {
//       const { error } = await deleteProfessionalTopics(token, clickTopic.topic_name)
//       if (error) {
//         console.error(error)
//       }
//       setOpenModal(false)
//       await fetchTopicsData()
//     } catch (err) {
//       console.error(err)
//     }
//   }

//   const handleOpenModal = (topic) => {
//     setClickTopic(topic)
//     setOpenModal(true)
//   }

//   return (
//     <Box>
//       <Typography variant="h6">Editá tus tópicos:</Typography>

//       {loading && <Typography>Cargando...</Typography>}

//       {!loading && (
//         <>
//           <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
//             {initialTopics.map((topic) => (
//               <div
//                 key={topic.topic_name}
//                 onClick={() => handleOpenModal(topic)}
//                 style={{
//                   backgroundColor: '#1cb698',
//                   color: '#fff',
//                   padding: '6px 12px',
//                   borderRadius: '20px',
//                   fontSize: '0.9rem',
//                   cursor: 'pointer'
//                 }}
//               >
//                 {topic.topic_name + " $" + topic.price_class}
//               </div>
//             ))}
//           </div>
//           {notSelectedTopics.length > 0 ? <div> <ScheduleTopicsProfile
//             isEditable={false}
//             onChange={handleChangeTopics}
//             value={selectTopic}
//             topicsList={notSelectedTopics}
//           />

//           <InputPrice 
//             value={price} 
//             onChange={(newPrice) => setPrice(newPrice)} 
//             label="Precio del servicio"
//             currencySymbol="$"
//           />

//           <Button
//             variant="contained"
//             color="primary"
//             onClick={handleConfirmChanges}
//             sx={{ marginTop: 2 }}
//           >
//             Agregar tópico
//           </Button> </div> : <p>Ya tiene todo los tópicos asignados</p>}
          

//           <ModalProfile
//             open={openModal}
//             onClose={() => setOpenModal(false)}
//             topic={clickTopic?.topic_name}
//             currentPrice={clickTopic?.price_class}
//             onSave={handleUpdatePrice}
//             onDelete={handleDeleteTopic}
//           />
//           {statusMessage && (
//             <Typography color="secondary" sx={{ marginTop: 2 }}>
//               {statusMessage}
//             </Typography>
//           )}
//         </>
//       )}
//     </Box>
//   );
// }
import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Chip,
  Typography,
  Divider,
  Paper,
} from '@mui/material';

import {
  getProfessionalTopics,
  postProfessionalTopics,
  deleteProfessionalTopics,
  putProfesionalTopics,
} from '../services/professionals-topic/professionals-topic.service.js';

import { getTopics } from '../services/topics/topics.service';
import ScheduleTopicsProfile from './profile/ScheduleTopicsProfile.jsx';
import InputPrice from './profile/InputPrice.jsx';
import ModalProfile from './profile/ModalProfile.jsx';

export default function ProfessionalAddTopic({ token }) {
  const [allTopics, setAllTopics] = useState([]);
  const [initialTopics, setInitialTopics] = useState([]);
  const [selectTopic, setSelectTopic] = useState([]);
  const [clickTopic, setClickTopic] = useState({});
  const [openModal, setOpenModal] = useState(false);
  const [price, setPrice] = useState(0);
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

      setAllTopics(all || []);
      setInitialTopics(assigned || []);
      setPrice(0);
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
    setSelectTopic(data);
  };

  const handleConfirmChanges = async () => {
    try {
      setLoading(true);
      setStatusMessage('');

      const { error } = await postProfessionalTopics(token, selectTopic, price);
      if (error) {
        setStatusMessage(`Error al agregar el tópico`);
        return;
      }
      await fetchTopicsData();
    } catch (error) {
      console.error('Error al aplicar cambios:', error);
      setStatusMessage('Error al aplicar cambios');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdatePrice = async (topic) => {
    try {
      const { error } = await putProfesionalTopics(token, topic);
      if (error) console.error(error);
      setOpenModal(false);
      await fetchTopicsData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteTopic = async () => {
    try {
      const { error } = await deleteProfessionalTopics(token, clickTopic.topic_name);
      if (error) console.error(error);
      setOpenModal(false);
      await fetchTopicsData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenModal = (topic) => {
    setClickTopic(topic);
    setOpenModal(true);
  };

  return (
    <Box
      sx={{
        backgroundColor: '#ECECDD',
        padding: 4,
        borderRadius: 3,
        boxShadow: 3,
        maxWidth: 700,
        margin: 'auto'
      }}
    >
      <Typography variant="h5" mb={3} sx={{ fontWeight: 'bold', textAlign: 'center' }}>
        Editá tus tópicos
      </Typography>

      {loading && <Typography>Cargando...</Typography>}

      {!loading && (
        <>
          <Paper elevation={0} sx={{ p: 2, backgroundColor: '#E4E3CD', mb: 3 }}>
            <Typography fontWeight="bold" mb={1}>Tópicos actuales:</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {initialTopics.map((topic) => (
                <Chip
                  key={topic.topic_name}
                  label={`${topic.topic_name} - $${topic.price_class}`}
                  onClick={() => handleOpenModal(topic)}
                  sx={{
                    backgroundColor: '#1cb698',
                    color: '#fff',
                    cursor: 'pointer',
                    fontWeight: 500,
                  }}
                />
              ))}
            </Box>
          </Paper>

          <Divider sx={{ mb: 3 }} />

          <Box>
            <Typography fontWeight="bold" mb={1}>Agregar nuevos tópicos:</Typography>
            <ScheduleTopicsProfile
              isEditable={false}
              onChange={handleChangeTopics}
              value={selectTopic}
              topicsList={allTopics}
            />

            <InputPrice
              value={price}
              onChange={(newPrice) => setPrice(newPrice)}
              label="Precio del servicio"
              currencySymbol="$"
            />

            <Button
              variant="contained"
              fullWidth
              onClick={handleConfirmChanges}
              sx={{
                marginTop: 2,
                backgroundColor: '#1cb698',
                '&:hover': {
                  backgroundColor: '#179e86'
                }
              }}
            >
              Agregar tópico
            </Button>
          </Box>

          <ModalProfile
            open={openModal}
            onClose={() => setOpenModal(false)}
            topic={clickTopic?.topic_name}
            currentPrice={clickTopic?.price_class}
            onSave={handleUpdatePrice}
            onDelete={handleDeleteTopic}
          />

          {statusMessage && (
            <Typography color="error" sx={{ marginTop: 2 }}>
              {statusMessage}
            </Typography>
          )}
        </>
      )}
    </Box>
  );
}

