import * as React from 'react';
import { Box, Typography, TextField } from '@mui/material';
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

export default function ScheduleTime({ value, onChange, isEditable }) {
  const { start, end } = value || {};

  console.log(value);
  // Helper para parsear string 'HH:MM:00:000Z' a Date
  const parseTime = (timeStr) => {
    if (!timeStr) return null;
    try {
      // Asumimos formato 'HH:mm:00.000' (sin Z)
      const [hours, minutes] = timeStr.split(':');
      const now = new Date();
      return new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate(),
        parseInt(hours, 10),
        parseInt(minutes, 10),
        0,
        0
      );
    } catch {
      return null;
    }
  };

  const formatTime = (date) => {
    if (!(date instanceof Date) || isNaN(date)) return '';
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}:00.000Z`;  // **Sin la Z**
  };

  const handleStartChange = (newValue) => {
    onChange?.({
      ...value,
      start: newValue ? formatTime(newValue) : '',
    });
  };

  const handleEndChange = (newValue) => {
    onChange?.({
      ...value,
      end: newValue ? formatTime(newValue) : '',
    });
  };

  console.log(start);
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1">
            <strong>Horario:</strong>{' '}
            {!end
              ? (start?.slice(0, 5) || '--:--') + 'hs'
              : `${start?.slice(0, 5) || '--:--'}hs - ${end?.slice(0, 5) || '--:--'}hs`}
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
