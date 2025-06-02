import * as React from 'react';
import { useEffect } from 'react';
import {
  Box, Typography, TextField
} from '@mui/material';
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format, isValid as isDateValid } from 'date-fns';
import { useAuth0 } from '@auth0/auth0-react';

export default function ScheduleTime(props) {
  const { taskData, isEditable, onChangeData } = props;
  const { getAccessTokenSilently, isAuthenticated } = useAuth0()

  const [startTime, setStartTime] = React.useState(null);
  const [endTime, setEndTime] = React.useState(null);

  useEffect(() => {
    // Para edición (formato con strings de hora) 
    if (taskData?.day && taskData?.start && typeof taskData.start === 'string') {
      // Eliminar "undefinedT" si existe
      const cleanStart = taskData.start.replace('undefinedT', '');
      const cleanEnd = taskData.end.replace('undefinedT', '');
      
      const startDate = new Date(`${taskData.day}T${cleanStart}`);
      const endDate = new Date(`${taskData.day}T${cleanEnd}`);
      
      setStartTime(isDateValid(startDate) ? startDate : null);
      setEndTime(isDateValid(endDate) ? endDate : null);
    }
    // Para creación (formato con objetos Date)
    else if (taskData?.start instanceof Date) {
      setStartTime(isDateValid(taskData.start) ? taskData.start : null);
      setEndTime(isDateValid(taskData.end) ? taskData.end : null);
    }
    else if (taskData.week_day != null){
      setStartTime(taskData.start);
      setEndTime(taskData.end)
    }
    else {
      // Caso por defecto (sin datos)
      const now = new Date();
      setStartTime(now);
      setEndTime(new Date(now.getTime() + 60 * 60 * 1000)); // +1 hora
    }
  }, [taskData]);

  const formatTimeForAPI = (date) => {
    if (!date || !isDateValid(date)) return '00:00:00';
    return format(date, 'HH:mm:ss');
  };
    
  const handleStartChange = (newValue) => {
    if (isDateValid(newValue)) {
      setStartTime(newValue);
      onChangeData?.({ 
        start: formatTimeForAPI(newValue),
        // Mantenemos el día original para edición
        day: taskData?.day || format(newValue, 'yyyy-MM-dd')
      });
      
      // Ajustar automáticamente el endTime si es anterior
      if (endTime && newValue > endTime) {
        const newEndTime = new Date(newValue.getTime() + 60 * 60 * 1000);
        setEndTime(newEndTime);
        onChangeData?.({ 
          end: formatTimeForAPI(newEndTime)
        });
      }
    }
  };

  const handleEndChange = (newValue) => {
    if (isDateValid(newValue)) {
      setEndTime(newValue);
      onChangeData?.({ 
        end: formatTimeForAPI(newValue)
      });
    }
  };
    
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1">
            <strong>Horario:</strong> {formatTimeForDisplay(startTime)} - {formatTimeForDisplay(endTime)}
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

// Función separada para formato de visualización
function formatTimeForDisplay(date) {
  if (typeof date === 'string') return date;
  if (!date || !isDateValid(date)) return '--:--';
  return format(date, 'HH:mm');
}