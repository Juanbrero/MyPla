import * as React from 'react';
import {
  Box, Typography, Checkbox, MenuItem, Select, ListItemText, FormControl, InputLabel, Chip
} from '@mui/material';

export default function Topics({ value = [], onChange, isEditable, topicsList = [] }) {

  const handleChange = (event) => {
    const newTopics = typeof event.target.value === 'string' ? event.target.value.split(',') : event.target.value;
    onChange?.(newTopics);
  };

  if (!isEditable) {
    return (
      <Box>
        <Typography variant="subtitle1"><strong>Tópicos asignados:</strong></Typography>
        {value.length > 0 ? (
          value.map((topic) => (
            <Chip key={topic} label={topic} sx={{ marginRight: 1, marginBottom: 1 }} />
          ))
        ) : (
          <Typography>No asignado</Typography>
        )}
      </Box>
    );
  }

  return (
    <FormControl fullWidth margin="normal">
      <InputLabel>Temas disponibles</InputLabel>
      <Select
        multiple
        value={value}
        onChange={handleChange}
        renderValue={(selected) => selected.join(', ')}
        label="Temas disponibles"
      >
        {topicsList.map((topic) => (
          <MenuItem key={topic} value={topic}>
            <Checkbox checked={value.indexOf(topic) > -1} />
            <ListItemText primary={topic} />
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
