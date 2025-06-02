import * as React from 'react';
import { Box, Typography, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

const DAYS = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

export default function ScheduleDate({ type, value, onChange, isEditable }) {
  // value = { week_day: number (0-6) } || { date: 'YYYY-MM-DD' }

  const handleDayChange = (event) => {
    const dayIndex = DAYS.indexOf(event.target.value);
    onChange?.({ week_day: dayIndex });
  };

  const handleDateChange = (newValue) => {
    if (!(newValue instanceof Date) || isNaN(newValue)) return;
    const formatted = format(newValue, 'yyyy-MM-dd'); // en tu zona horaria
    onChange?.({ date: formatted });
  };

  const renderContent = () => {
    if (!isEditable) {
      return (
        <Box>
          <Typography variant="subtitle1">
            <strong>{type === 'recurrent' ? 'Día' : 'Fecha'}:</strong>{' '}
            {type === 'recurrent'
              ? DAYS[value?.week_day  ?? 0]
              : value?.date
                ? format(parseISO(value.date), 'dd-MM-yyyy')
                : '--/--/----'}
          </Typography>
        </Box>
      );
    }

    if (type === 'recurrent') {
      return (
        <FormControl fullWidth margin="normal">
          <InputLabel>Día</InputLabel>
          <Select
            value={DAYS[value?.week_day  ?? 0]}
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
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <DatePicker
          label="Fecha"
          value={
            value?.date
              ? (() => {
                  const [year, month, day] = value.date.split('-');
                  return new Date(year, month - 1, day);
                })()
              : null
          }
          onChange={handleDateChange}
          inputFormat="dd-MM-yyyy"
          slotProps={{ textField: { fullWidth: true, margin: 'normal' } }}
        />
      </LocalizationProvider>
    );
  };

  return <>{renderContent()}</>;
}
