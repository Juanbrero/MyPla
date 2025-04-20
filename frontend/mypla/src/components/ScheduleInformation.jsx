import * as React from 'react';
import {
  Box, Button, Typography, Modal, TextField, Checkbox, FormControlLabel,
  MenuItem, Select, ListItemText, FormControl, InputLabel
} from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { es } from 'date-fns/locale'; // Español opcional
import { useEffect } from 'react'

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 500,
  bgcolor: 'background.paper',
  borderRadius: '12px',
  boxShadow: 24,
  p: 4,
  color: 'text.primary',
};

const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
const topics = ['Estrategia', 'Marketing', 'Ventas', 'Finanzas', 'Recursos Humanos'];

export default function ScheduleInformation({
  open,
  onClose,
  taskData,
  // onCancelSlot,
  onCancelTask,
  onSaveTask,
}) {
  const [selectedTopicsState, setSelectedTopicsState] = React.useState(taskData?.topics || []);
  const [day, setDay] = React.useState(taskData?.day || 'Lunes');
  const [startTime, setStartTime] = React.useState(taskData?.startTime || '09:00');
  const [endTime, setEndTime] = React.useState(taskData?.endTime || '10:00');
  const [isRecurring, setIsRecurring] = React.useState(taskData?.recurrent || false);
  const [selectedDate, setSelectedDate] = React.useState(
    taskData?.date ? new Date(taskData.date) : new Date()
  );

  useEffect(() => {
    setSelectedTopicsState(taskData?.topics || []);
    setDay(taskData?.day || 'Lunes');
    setStartTime(taskData?.start || '09:00');
    setEndTime(taskData?.end || '10:00');
    setIsRecurring(taskData?.recurrent || false);
    if (taskData.date) {
      const [year, month, day] = taskData.date.split("-");
      const generateDate = new Date(year, month - 1, day);
      setSelectedDate(generateDate);
    } else {
      setSelectedDate(new Date());
    }
  }, [taskData]);
  

  const handleTopicChange = (event) => {
    const { target: { value } } = event;
    setSelectedTopicsState(typeof value === 'string' ? value.split(',') : value);
  };

  // const handleCancelSlot = () => {
  //   onCancelSlot?.({ day, startTime, endTime });
  // };

  const handleCancelTask = () => {
    onCancelTask?.(selectedTopicsState);
  };

  const handleSaveTask = () => {
    if (!selectedTopicsState.length || !startTime || !endTime) {
      alert('Por favor complete todos los campos');
      return;
    }
    if (startTime >= endTime) {
      alert('La hora de inicio no puede ser mayor o igual que la de fin');
      return;
    }

    onSaveTask?.({
      ...taskData,
      topics: selectedTopicsState,
      day: isRecurring ? day : null,
      date: isRecurring ? null : selectedDate?.toISOString(),
      startTime,
      endTime,
      isRecurring,
    });
  };

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>Editar Horario</Typography>

          {/* Tópicos */}
          <FormControl fullWidth margin="normal">
            <InputLabel>Tópicos posibles</InputLabel>
            <Select
              multiple
              value={selectedTopicsState}
              onChange={handleTopicChange}
              renderValue={(selected) => selected.join(', ')}
              label="Tópicos posibles"
            >
              {topics.map((topic) => (
                <MenuItem key={topic} value={topic}>
                  <Checkbox checked={selectedTopicsState.indexOf(topic) > -1} />
                  <ListItemText primary={topic} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Día o Fecha */}
          {isRecurring ? (
            <FormControl fullWidth margin="normal">
              <InputLabel>Día</InputLabel>
              <Select
                value={day}
                onChange={(e) => setDay(e.target.value)}
                label="Día"
              >
                {days.map((d) => (
                  <MenuItem key={d} value={d}>{d}</MenuItem>
                ))}
              </Select>
            </FormControl>
          ) : (
            <DatePicker
              label="Fecha"
              value={selectedDate}
              onChange={(newValue) => setSelectedDate(newValue)}
              slotProps={{ textField: { fullWidth: true, margin: 'normal' } }}
            />
          )}

          {/* Horario */}
          <Box display="flex" gap={2} mt={2} flexDirection={{ xs: 'column', sm: 'row' }}>
            <TextField
              type="time"
              label="Inicio"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              type="time"
              label="Fin"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Box>

          {/* Recurrente */}
          <FormControlLabel
            control={
              <Checkbox
                checked={isRecurring}
                onChange={(e) => setIsRecurring(e.target.checked)}
              />
            }
            label="Repetir semanalmente"
            sx={{ mt: 2 }}
          />

          {/* Botones */}
          <Box display="flex" justifyContent="flex-end" flexDirection={{ xs: 'column', sm: 'row' }} gap={2} mt={3}>
            {/* <Button color="warning" variant="outlined" onClick={handleCancelSlot} fullWidth sx={{ mb: { xs: 1, sm: 0 } }}>
              Cancelar esta franja
            </Button> */}
            <Button color="error" variant="contained" onClick={handleCancelTask} fullWidth sx={{ p: 2 }}>
              Cancelar toda la tarea
            </Button>
            <Button color="primary" variant="contained" onClick={handleSaveTask} fullWidth sx={{ p: 2 }}>
              Guardar cambios
            </Button>
          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}
