import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Chip,
  Typography,
  Divider,
  Paper,
  Checkbox,
  FormControlLabel,
} from '@mui/material';

import {
  getProfessionalTopics,
  postProfessionalTopics,
  deleteProfessionalTopics,
  putProfesionalTopics,
} from '../services/professionals-topic/professionals-topic.service.js';

import { getTopics, getTopicsByCategory } from '../services/topics/topics.service';
import { getCategories } from '../services/categories/category.service';

import InputPrice from './profile/InputPrice.jsx';
import ModalProfile from './profile/ModalProfile.jsx';

export default function ProfessionalAddTopic({ token }) {
  const [allTopics, setAllTopics] = useState([]);
  const [initialTopics, setInitialTopics] = useState([]);
  const [selectTopic, setSelectTopic] = useState([]); // array de topic_name string
  const [clickTopic, setClickTopic] = useState({});
  const [openModal, setOpenModal] = useState(false);
  const [price, setPrice] = useState(0);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [searchByCategory, setSearchByCategory] = useState(false);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');

  const fetchTopicsData = async () => {
    try {
      setLoading(true);
      const { data: all } = await getTopics();
      const assigned = await getProfessionalTopics(token, true);
      setAllTopics(all || []);
      setInitialTopics(assigned || []);
      setPrice(0);
    } catch (error) {
      console.error('Error al obtener datos de tópicos:', error);
      setStatusMessage('Error inesperado');
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const { data } = await getCategories();
      setCategories(data || []);
    } catch (error) {
      console.error('Error al obtener categorías:', error);
    }
  };

  const fetchTopicsByCategory = async (category) => {
    
    try {
      const { data } = await getTopicsByCategory(category);
      // Aquí valida que data sea array de tópicos con topic_name
      if (!Array.isArray(data)) {
        console.warn('fetchTopicsByCategory data no es array:', data);
        setAllTopics([]);
      } else {
        setAllTopics(data);
      }
    } catch (error) {
      console.error('Error al obtener tópicos por categoría:', error);
      setAllTopics([]);
    }
  };

  useEffect(() => {
    if (token) fetchTopicsData();
  }, [token]);

  useEffect(() => {
    if (searchByCategory) {
      fetchCategories();
      setAllTopics([]);
    } else {
      fetchTopicsData();
      setSelectedCategory('');
    }
    setSelectTopic([]);
  }, [searchByCategory]);

  useEffect(() => {
    if (selectedCategory) {
      fetchTopicsByCategory(selectedCategory);
      setSelectTopic([]);
    }
  }, [selectedCategory]);

  // Manejador checkbox sin recarga
  const handleSearchByCategoryChange = (event) => {
    event.preventDefault(); // en teoría no hace falta, pero por si acaso
    setSearchByCategory(event.target.checked);
  };

  const handleSelectChange = (e) => {
    const value = e.target.value;
    if (value.startsWith('categoria:')) {
      const cat = value.replace('categoria:', '');
      setSelectedCategory(cat);
      setSelectTopic([]); // limpia selección de tópico
    } else if (value.startsWith('topico:')) {
      const topic = value.replace('topico:', '');
      setSelectTopic([topic]);
    } else {
      setSelectTopic([]);
    }
  };

  const handleConfirmChanges = async () => {
    try {
      setLoading(true);
      setStatusMessage('');
      console.log(selectTopic[0]);
      const { error } = await postProfessionalTopics(token, selectTopic[0], price);
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

  console.log('allTopics:', allTopics);

  return (
    <Box
      sx={{
        backgroundColor: '#ECECDD',
        padding: 4,
        borderRadius: 3,
        boxShadow: 3,
        maxWidth: 700,
        margin: 'auto',
      }}
    >
      <Typography variant="h5" mb={3} sx={{ fontWeight: 'bold', textAlign: 'center' }}>
        Editá tus tópicos
      </Typography>

      {loading && <Typography>Cargando...</Typography>}

      {!loading && (
        <>
          {/* Chips actuales (tópicos asignados) */}
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

          {/* Checkbox para buscar por categoría */}
          <Box sx={{ mb: 1, position: 'relative' }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={searchByCategory}
                  onChange={handleSearchByCategoryChange}
                  size="small"
                />
              }
              label={<Typography variant="body2">Buscar por categoría</Typography>}
              sx={{
                position: 'absolute',
                top: -30,
                left: 0,
              }}
            />
          </Box>

          {/* Chip categoría seleccionada encima del select */}
          {searchByCategory && selectedCategory && (
            <Box sx={{ mb: 1 }}>
              <Chip
                label={selectedCategory}
                onDelete={() => setSelectedCategory('')}
                sx={{ backgroundColor: '#D4DDD6' }}
              />
            </Box>
          )}

          {/* Select para categorías o tópicos */}
          <Box sx={{ mb: 2 }}>
            
            <select
              value={
                searchByCategory
                  ? (selectTopic.length > 0
                      ? `topico:${selectTopic[0]}`
                      : selectedCategory
                      ? `categoria:${selectedCategory}`
                      : '')
                  : (selectTopic.length > 0 ? `topico:${selectTopic[0]}` : '')
              }
              onChange={handleSelectChange}
              style={{ width: '100%', padding: 10 }}
            >
              <option value="">
                {searchByCategory
                  ? selectedCategory
                    ? 'Seleccionar tópico...'
                    : 'Seleccionar categoría...'
                  : 'Seleccionar tópico...'}
              </option>

              {/* Opciones de categorías si está activo filtro */}
              {searchByCategory && !selectedCategory &&
                categories.map((cat, i) => (
                  <option key={`cat-${i}`} value={`categoria:${cat}`}>
                    {cat}
                  </option>
                ))}

              {/* Opciones de tópicos si categoría seleccionada */}
              {searchByCategory && selectedCategory &&
                allTopics.map((t, i) => (
                  <option key={`topico-${i}`} value={`topico:${t}`}>
                    {t}
                  </option>
                ))}

              {/* Opciones de tópicos sin filtro por categoría */}
              {!searchByCategory &&
                allTopics.map((t, i) => (
                  <option key={`all-${i}`} value={`topico:${t}`}>
                    {t}
                  </option>
                ))}
            </select>
          </Box>

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
              mt: 2,
              backgroundColor: '#1cb698',
              '&:hover': { backgroundColor: '#179e86' },
            }}
          >
            Agregar tópico
          </Button>

          <ModalProfile
            open={openModal}
            onClose={() => setOpenModal(false)}
            topic={clickTopic?.topic_name}
            currentPrice={clickTopic?.price_class}
            onSave={handleUpdatePrice}
            onDelete={handleDeleteTopic}
          />

          {statusMessage && (
            <Typography color="error" sx={{ mt: 2 }}>
              {statusMessage}
            </Typography>
          )}
        </>
      )}
    </Box>
  );
}
