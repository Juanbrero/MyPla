import * as React from 'react';
import {
  Box, Button, Typography, Modal, TextField, Checkbox, FormControlLabel,
  MenuItem, Select, ListItemText, FormControl, InputLabel, Chip
} from '@mui/material';
import { DatePicker, TimePicker, LocalizationProvider } from '@mui/x-date-pickers';
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
  onCancelTask,
  onSaveTask,
  onDeleteTask,
  onCancelOneOccurrence,
}) {
  const [selectedTopicsState, setSelectedTopicsState] = React.useState(taskData?.topics || []);
  const [day, setDay] = React.useState(taskData?.day || 'Lunes');
  const [startTime, setStartTime] = React.useState(taskData?.start ? new Date(`1970-01-01T${taskData.start}:00`) : null);
  const [endTime, setEndTime] = React.useState(taskData?.end ? new Date(`1970-01-01T${taskData.end}:00`) : null);
  const [isRecurring, setIsRecurring] = React.useState(taskData?.recurrent || false);
  const [selectedDate, setSelectedDate] = React.useState(taskData?.date ? new Date(taskData.date) : new Date());
  const [isEditable, setIsEditable] = React.useState(false); // Controla si el formulario es editable

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

  const handleCancelTask = () => {
    onCancelTask?.(taskData);
  };

  const handleCancelOneOccurrence = () => {
    onCancelOneOccurrence?.(taskData);
  };

  const handleDeleteTask = () => {
    onDeleteTask?.(taskData);
  };

  const formatTime = (date) => {
    if (!(date instanceof Date)) return date
    date.toTimeString().slice(0, 5)
  } // 'HH:MM'

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
      startTime: formatTime(startTime),
      endTime: formatTime(endTime),
      isRecurring,
    });
    setIsEditable(false); // Regresar al modo de solo lectura después de guardar
  };

  const handleCancelChanges = () => {
    setIsEditable(false); // Regresar al modo de solo lectura
    setSelectedTopicsState(taskData?.topics || []);
    setDay(taskData?.day || 'Lunes');
    setStartTime(taskData?.startTime ? new Date(`1970-01-01T${taskData.startTime}`) : new Date());
    setEndTime(taskData?.endTime ? new Date(`1970-01-01T${taskData.endTime}`) : new Date());
    setIsRecurring(taskData?.recurrent || false);
    setSelectedDate(taskData?.date ? new Date(taskData.date) : new Date());
  };

  const handleEditSchedule = () => {
    setIsEditable(true); // Permite editar el horario
  };

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>Información del Horario</Typography>

          {/* Topicos */}
          {!isEditable ? (
            <Box>
              <Typography variant="subtitle1"><strong>Posibles topicos:</strong></Typography>
              {selectedTopicsState.length ? (
                selectedTopicsState.map((topic) => (
                  <Chip key={topic} label={topic} sx={{ marginRight: 1, marginBottom: 1 }} />
                ))
              ) : (
                <Typography>No asignado</Typography>
              )}
            </Box>
          ) : (
            <FormControl fullWidth margin="normal">
              <InputLabel>Posibles topicos</InputLabel>
              <Select
                multiple
                value={selectedTopicsState}
                onChange={handleTopicChange}
                renderValue={(selected) => selected.join(', ')}
                label="Posibles topicos"
              >
                {topics.map((topic) => (
                  <MenuItem key={topic} value={topic}>
                    <Checkbox checked={selectedTopicsState.indexOf(topic) > -1} />
                    <ListItemText primary={topic} />
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}

          {/* Día o Fecha */}
          {!isEditable ? (
            <Box>
              <Typography variant="subtitle1"><strong>{isRecurring ? 'Día' : 'Fecha'}:</strong> 
                {isRecurring ? day : selectedDate.toLocaleDateString()}
              </Typography>
            </Box>
          ) : (
            isRecurring ? (
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
            )
          )}

          {/* Horario */}
          {!isEditable ? (
            <Box>
              <Typography variant="subtitle1"><strong>Horario:</strong> {formatTime(startTime)} - {formatTime(endTime)}</Typography>
            </Box>
          ) : (
            <Box display="flex" gap={2} mt={2} flexDirection={{ xs: 'column', sm: 'row' }}>
              <TimePicker
                label="Inicio"
                value={startTime}
                onChange={(newValue) => setStartTime(newValue)}
                minutesStep={30}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
              <TimePicker
                label="Fin"
                value={endTime}
                onChange={(newValue) => setEndTime(newValue)}
                minutesStep={30}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </Box>
          )}

          {/* Recurrente */}
          {!isEditable ? (
            <Box>
              <Typography variant="subtitle1"><strong>Es recurrente:</strong> {isRecurring ? 'Sí' : 'No'}</Typography>
            </Box>
          ) : (
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
          )}

          {/* Botones */}
          <Box display="flex" justifyContent="flex-end" flexDirection={{ xs: 'column', sm: 'row' }} gap={2} mt={3}>
            {!isEditable ? (
              <>
                {isRecurring && (
                  <Button color="error" variant="outlined" onClick={handleCancelOneOccurrence} fullWidth sx={{ p: 2 }}>
                    Cancelar solo esta vez
                  </Button>
                )}
                <Button color="primary" variant="contained" onClick={handleEditSchedule} fullWidth sx={{ p: 2 }}>
                  Editar tarea
                </Button>
              </>
            ) : (
              <>
                <Button color="error" variant="contained" onClick={handleDeleteTask} fullWidth sx={{ p: 2 }}>
                  Borrar tarea
                </Button>
                <Button color="secondary" variant="outlined" onClick={handleCancelChanges} fullWidth sx={{ p: 2 }}>
                  Cancelar cambios
                </Button>
                <Button color="primary" variant="contained" onClick={handleSaveTask} fullWidth sx={{ p: 2 }}>
                  Guardar cambios
                </Button>
              </>
            )}
          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}
