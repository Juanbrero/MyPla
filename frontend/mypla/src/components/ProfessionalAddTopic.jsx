import * as React from 'react';
import {
  Box, Typography, Checkbox, MenuItem, Select, ListItemText, FormControl, InputLabel, Chip
} from '@mui/material';
import { useEffect, useState } from 'react';
import { getTopics } from '../services/topics/topics.service';
import { getProfessionalsTopic } from '../services/professionals-topic/professionals-topic.service'


// Supongamos que tienes esta función:
    // const topics = getTopics()
    // const ownTopics = getProfessionalsTopic(token)

export default function Topics(props) {
  const { taskData, clickedEvent, isEditable, onChangeData } = props;

  const [selectedTopicsState, setSelectedTopicsState] = useState(taskData?.topics || []);
  const [editTopics, setEditTopics] = useState(clickedEvent?.extendedProps?.eventTopics || []);

  const topicsList = getTopics(); // Obtiene los temas

  useEffect(() => {
    if (taskData?.topics && Array.isArray(taskData.topics)) {
      setSelectedTopicsState(taskData.topics);
    }
    if (clickedEvent?.extendedProps?.eventTopics) {
      setEditTopics(clickedEvent.extendedProps.eventTopics);
    }
  }, [taskData?.topics, clickedEvent?.extendedProps?.eventTopics]);

  const handleTopicChange = (event) => {
    const { target: { value } } = event;
    const newTopics = typeof value === 'string' ? value.split(',') : value;
    setSelectedTopicsState(newTopics);
    onChangeData?.({ topics: newTopics });
  };

  return (
    <>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1"><strong>Topicos asignados:</strong></Typography>
          {editTopics.length ? (
            editTopics.map((topic) => (
              <Chip key={topic} label={topic} sx={{ marginRight: 1, marginBottom: 1 }} />
            ))
          ) : (
            <Typography>No asignado</Typography>
          )}
        </Box>
      ) : (
        <FormControl fullWidth margin="normal">
          <InputLabel>Posibles tópicos</InputLabel>
          <Select
            multiple
            value={selectedTopicsState}
            onChange={handleTopicChange}
            renderValue={(selected) => selected.join(', ')}
            label="Posibles tópicos"
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
