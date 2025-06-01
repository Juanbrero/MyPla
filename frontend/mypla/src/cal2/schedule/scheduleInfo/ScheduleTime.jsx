import * as React from 'react';
import { Box, Typography, TextField } from '@mui/material';
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

export default function ScheduleTime({ value, onChange, isEditable }) {
  const { start, end } = value || {};

  // Helper para parsear string 'HH:mm' a Date
  const parseTime = (timeStr) => {
    if (!timeStr) return null;
    const [hours, minutes] = timeStr.split(':').map(Number);
    const date = new Date();
    date.setHours(hours);
    date.setMinutes(minutes);
    date.setSeconds(0);
    date.setMilliseconds(0);
    return date;
  };

  // Helper para formatear Date a 'HH:mm'
  const formatTime = (date) => {
    if (!(date instanceof Date) || isNaN(date)) return '';
    return date.toTimeString().slice(0, 5); // HH:mm
  };

  const handleStartChange = (newValue) => {
    onChange?.({
      ...value,
      start: formatTime(newValue)
    });
  };

  const handleEndChange = (newValue) => {
    onChange?.({
      ...value,
      end: formatTime(newValue)
    });
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1">
            <strong>Horario:</strong> {start.slice(0, 5) || '--:--'} - {end.slice(0, 5) || '--:--'}
          </Typography>
        </Box>
      ) : (
        <Box display="flex" gap={2} mt={2} flexDirection={{ xs: 'column', sm: 'row' }}>
          <TimePicker
            label="Inicio"
            value={parseTime(start)}
            onChange={handleStartChange}
            minutesStep={30}
            ampm={false}
            inputFormat="HH:mm"
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
          <TimePicker
            label="Fin"
            value={parseTime(end)}
            onChange={handleEndChange}
            minutesStep={30}
            ampm={false}
            inputFormat="HH:mm"
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </Box>
      )}
    </LocalizationProvider>
  );
}
