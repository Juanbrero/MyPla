import * as React from 'react';
import {
  Box, Typography, Checkbox, MenuItem, Select, ListItemText, FormControl, InputLabel, Chip
} from '@mui/material';

export default function ScheduleTopicsProfile({ value = [], onChange, topicsList = [] }) {

  const handleChange = (event) => {
    onChange(event.target.value)
  };

  return (
    <FormControl fullWidth margin="normal">
      <InputLabel>Temas disponibles</InputLabel>
      <Select
        value={value}
        onChange={handleChange}
        label="Temas disponibles"
      >
      {Array.isArray(topicsList) ? (
        topicsList.map((topic) => (
          <MenuItem key={topic} value={topic}>
            <ListItemText primary={topic} />
          </MenuItem>
        ))
      ) : (
        <Typography color="error">No hay temas disponibles</Typography>
      )}
      </Select>
    </FormControl>
  );
}
