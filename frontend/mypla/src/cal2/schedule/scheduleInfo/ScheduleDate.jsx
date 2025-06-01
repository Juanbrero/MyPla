import * as React from 'react';
import { Box, Typography, MenuItem, Select, FormControl, InputLabel, TextField } from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

const DAYS = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

export default function ScheduleDate({ type, value, onChange, isEditable }) {
  // value = { week_day: number (0-6) } || { date: 'YYYY-MM-DD' }

  const handleDayChange = (event) => {
    const dayIndex = DAYS.indexOf(event.target.value);
    onChange?.({ week_day: dayIndex });
  };

  const handleDateChange = (newValue) => {
    if (!(newValue instanceof Date) || isNaN(newValue)) return;
    const formatted = newValue.toISOString().slice(0, 10); // 'YYYY-MM-DD'
    onChange?.({ date: formatted });
  };

  const renderContent = () => {
    if (!isEditable) {
      return (
        <Box>
          <Typography variant="subtitle1">
            <strong>{type === 'recurrent' ? 'Día' : 'Fecha'}:</strong>{' '}
            {type === 'recurrent'
              ? DAYS[value?.week_day ?? 0]
              : value?.date ?? '--/--/----'}
          </Typography>
        </Box>
      );
    }

    if (type === 'recurrent') {
      return (
        <FormControl fullWidth margin="normal">
          <InputLabel>Día</InputLabel>
          <Select
            value={DAYS[value?.week_day ?? 0]}
            onChange={handleDayChange}
            label="Día"
          >
            {DAYS.map((d) => (
              <MenuItem key={d} value={d}>{d}</MenuItem>
            ))}
          </Select>
        </FormControl>
      );
    }

    // specific
    return (
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <DatePicker
          label="Fecha"
          value={value?.date ? new Date(value.date) : null}
          onChange={handleDateChange}
          slotProps={{ textField: { fullWidth: true, margin: 'normal' } }}
        />
      </LocalizationProvider>
    );
  };

  return <>{renderContent()}</>;
}
