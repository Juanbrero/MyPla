import * as React from 'react';
import {
  Box, Typography, Checkbox, MenuItem, Select, ListItemText, FormControl, InputLabel, Chip
} from '@mui/material';
import { useEffect } from 'react'

const TOPICS = ['Estrategia', 'Marketing', 'Ventas', 'Finanzas', 'Recursos Humanos'];

export default function Topics(props) {
  const { taskData, isEditable, onChangeData } = props;

  const [selectedTopicsState, setSelectedTopicsState] = React.useState(taskData?.topics || []);
  console.log("creando componentes");
  
  useEffect(() => {
    if (taskData?.topics && Array.isArray(taskData.topics)) {
      setSelectedTopicsState(taskData.topics);
    }
  }, [taskData?.topics]);


  const handleTopicChange = (event) => {
      const { target: { value } } = event;
      const newTopics = typeof value === 'string' ? value.split(',') : value;
      setSelectedTopicsState(newTopics);
      onChangeData?.({ topics : newTopics});
  };

  return (
    <>
    {!isEditable ? (
      <Box>
      <Typography variant="subtitle1"><strong>Posibles topicos:</strong></Typography>
      {selectedTopicsState.length ? (
        selectedTopicsState.map((topic) => (
          <Chip key={topic} label={topic} sx={{ marginRight: 1, marginBottom: 1 }} />
        ))
      ) : (
        <Typography>No asignado</Typography>
      )}
      </Box>
    ) : (
      <FormControl fullWidth margin="normal">
      <InputLabel>Posibles topicos</InputLabel>
      <Select
      multiple
      value={selectedTopicsState}
      onChange={handleTopicChange}
      renderValue={(selected) => selected.join(', ')}
      label="Posibles topicos"
      >
      {TOPICS.map((topic) => (
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