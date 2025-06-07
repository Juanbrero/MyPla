import * as React from 'react';
import {
  Box, Typography, MenuItem, Select, ListItemText, FormControl, InputLabel, Chip
} from '@mui/material';

export default function ScheduleTopicsReservation({ value = '', onChange, isEditable, topicsList = [] }) {

  const handleChange = (event) => {
    const selected = event.target.value;
    onChange?.(selected);
  };

  if (!isEditable) {
    return (
      <Box>
        <Typography variant="subtitle1"><strong>Tópico asignado:</strong></Typography>
        {value ? (
          <Chip label={value} sx={{ marginRight: 1, marginBottom: 1 }} />
        ) : (
          <Typography>No asignado</Typography>
        )}
      </Box>
    );
  }

  return (
    <FormControl fullWidth margin="normal">
      <InputLabel id="topics-label">Temas disponibles</InputLabel>
      <Select
        labelId="topics-label"
        value={value}
        onChange={handleChange}
        label="Temas disponibles"
      >
        {topicsList.length > 0 ? (
          topicsList.map((topic) => (
            <MenuItem key={topic} value={topic}>
              <ListItemText primary={topic} />
            </MenuItem>
          ))
        ) : (
          <MenuItem disabled>No hay temas disponibles</MenuItem>
        )}
      </Select>
    </FormControl>
  );
}
