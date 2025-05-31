import * as React from 'react';
import {
  Box, Typography, Checkbox, MenuItem, Select, ListItemText, FormControl, InputLabel, Chip
} from '@mui/material';
import { useEffect, useState } from 'react';
import { getProfessionalsTopic } from '../../../services/professionals-topic/professionals-topic.service';

export default function Topics(props) {
  const { taskData, clickedEvent, isEditable, onChangeData, topicsListFromParent } = props;

  console.log(taskData)

  const [selectedTopicsState, setSelectedTopicsState] = useState(taskData?.topics || []);
  const [editTopics, setEditTopics] = useState([]);
  const [topicsList, setTopicsList] = useState(topicsListFromParent || []);

  // Fetch topics si no vienen del padre
  useEffect(() => {
    if (!topicsListFromParent || topicsListFromParent.length === 0) {
      const fetchTopics = async () => {
        try {
          const { data, error } = await getProfessionalsTopic(); // usa el profId si hace falta
          if (error) {
            console.error('Error al obtener los tópicos:', error);
            return;
          }
          setTopicsList(data || []);
        } catch (err) {
          console.error('Error inesperado:', err);
        }
      };
      fetchTopics();
    }
  }, [topicsListFromParent]);

  // Actualizar selectedTopicsState si cambia taskData
  useEffect(() => {
    if (taskData?.topics && Array.isArray(taskData.topics)) {
      setSelectedTopicsState(taskData.topics);
    }
  }, [taskData?.topics]);

  // Actualizar editTopics según el tipo de evento
  useEffect(() => {
    if (!clickedEvent?.extendedProps) return;

    const { type, topics, topic } = clickedEvent.extendedProps;

    if (type === 'recurrent' || type === 'specific') {
      setEditTopics(Array.isArray(topics) ? topics : []);
    } else if (type === 'class_') {
      setEditTopics(topic ? [topic] : []);
    } else {
      setEditTopics([]);
    }
  }, [clickedEvent?.extendedProps]);

  // Actualizar topicsList si cambia desde el padre
  useEffect(() => {
    if (topicsListFromParent && topicsListFromParent.length > 0) {
      setTopicsList(topicsListFromParent);
    }
  }, [topicsListFromParent]);

  const handleTopicChange = (event) => {
    const { value } = event.target;
    const newTopics = typeof value === 'string' ? value.split(',') : value;
    setSelectedTopicsState(newTopics);
    onChangeData?.({ topics: newTopics });
  };

  return (
    <>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1"><strong>Tópicos asignados:</strong></Typography>
          {(taskData?.topics && taskData.topics.length > 0) ? (
            taskData.topics.map((topic) => (
              <Chip key={topic} label={topic} sx={{ marginRight: 1, marginBottom: 1 }} />
            ))
          ) : (
            <Typography>No asignado</Typography>
          )}
        </Box>
      ) : (
        <FormControl fullWidth margin="normal">
          <InputLabel>Temas disponibles</InputLabel>
          <Select
            multiple
            value={selectedTopicsState}
            onChange={handleTopicChange}
            renderValue={(selected) => selected.join(', ')}
            label="Temas disponibles"
          >
            {topicsList.map((topic) => (
              <MenuItem key={topic} value={topic}>
                <Checkbox checked={selectedTopicsState.indexOf(topic) > -1} />
                <ListItemText primary={topic} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )}
    </>
  );
}
