import * as React from 'react';
import { useEffect } from 'react';
import {
  Box, Typography, TextField
} from '@mui/material';
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format, parseISO, isValid as isDateValid } from 'date-fns';

export default function ScheduleTime(props) {
  const { taskData, clickedEvent, isEditable, onChangeData } = props;

  const [startTime, setStartTime] = React.useState(null);
  const [endTime, setEndTime] = React.useState(null);

  useEffect(() => {
    // Para edición (formato con strings de hora)
    if (taskData?.day && taskData?.start && typeof taskData.start === 'string') {
      const startDate = new Date(`${taskData.day}T${taskData.start}`);
      const endDate = new Date(`${taskData.day}T${taskData.end}`);
      
      setStartTime(isDateValid(startDate) ? startDate : null);
      setEndTime(isDateValid(endDate) ? endDate : null);
    }
    // Para creación (formato con objetos Date)
    else if (taskData?.start instanceof Date) {
      setStartTime(isDateValid(taskData.start) ? taskData.start : null);
      setEndTime(isDateValid(taskData.end) ? taskData.end : null);
    }
    // Caso por defecto (sin datos)
    else {
      const now = new Date();
      setStartTime(now);
      setEndTime(new Date(now.getTime() + 60 * 60 * 1000)); // +1 hora
    }
  }, [taskData]);

  const formatTime = (date) => {
    if (!date || !isDateValid(date)) return '--:--';
    return format(date, 'HH:mm');
  };
    
  const handleStartChange = (newValue) => {
    if (isDateValid(newValue)) {
      setStartTime(newValue);
      onChangeData?.({ 
        start: format(newValue, 'HH:mm:ss'),
        // Para mantener compatibilidad con ambos formatos
        startDate: newValue 
      });
      
      // Ajustar automáticamente el endTime si es anterior
      if (endTime && newValue > endTime) {
        const newEndTime = new Date(newValue.getTime() + 60 * 60 * 1000);
        setEndTime(newEndTime);
        onChangeData?.({ 
          end: format(newEndTime, 'HH:mm:ss'),
          endDate: newEndTime
        });
      }
    }
  };

  const handleEndChange = (newValue) => {
    if (isDateValid(newValue)) {
      setEndTime(newValue);
      onChangeData?.({ 
        end: format(newValue, 'HH:mm:ss'),
        endDate: newValue
      });
    }
  };
    
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1">
            <strong>Horario:</strong> {formatTime(startTime)} - {formatTime(endTime)}
          </Typography>
        </Box>
      ) : (
        <Box display="flex" gap={2} mt={2} flexDirection={{ xs: 'column', sm: 'row' }}>
          <TimePicker
            label="Inicio"
            value={startTime}
            onChange={handleStartChange}
            minutesStep={30}
            ampm={false}
            inputFormat="HH:mm"
            renderInput={(params) => (
              <TextField 
                {...params} 
                fullWidth 
                onKeyDown={(e) => e.stopPropagation()}
              />
            )}
          />
          <TimePicker
            label="Fin"
            value={endTime}
            onChange={handleEndChange}
            minutesStep={30}
            ampm={false}
            inputFormat="HH:mm"
            renderInput={(params) => (
              <TextField 
                {...params} 
                fullWidth
                onKeyDown={(e) => e.stopPropagation()}
              />
            )}
          />
        </Box>
      )}
    </LocalizationProvider>
  );
}