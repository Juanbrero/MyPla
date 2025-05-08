import * as React from 'react';
import {
  Box, Button, Typography, Modal, TextField, Checkbox, FormControlLabel,
  MenuItem, Select, ListItemText, FormControl, InputLabel
} from '@mui/material';
import { DatePicker, TimePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { es } from 'date-fns/locale';
import Topics from './schedule/scheduleInfo/Topics';
import ScheduleDate from './schedule/scheduleInfo/ScheduleDate';
import ScheduleTime from './schedule/scheduleInfo/ScheduleTime';
import Recurrent from './schedule/scheduleInfo/Recurrent';


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
}) {


  const handleCancelTask = () => {
    onCancelTask?.(selectedTopicsState);
  };

  const formatTime = (date) => date.toTimeString().slice(0, 5); // 'HH:MM'

  const handleSaveTask = () => {
    // if (!selectedTopicsState.length || !startTime || !endTime) {
    //   alert('Por favor complete todos los campos');
    //   return;
    // }

    // if (startTime >= endTime) {
    //   alert('La hora de inicio no puede ser mayor o igual que la de fin');
    //   return;
    // }

    // onSaveTask?.({
    //   ...taskData,
    //   topics: selectedTopicsState,
    //   day: isRecurring ? day : null,
    //   date: isRecurring ? null : selectedDate?.toISOString(),
    //   startTime: formatTime(startTime),
    //   endTime: formatTime(endTime),
    //   isRecurring,
    // });
  };

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>Editar Horario</Typography>

          <Topics 
            taskData={taskData}
            isEditable={true}
          />
          <ScheduleDate 
            taskData={taskData}
            isEditable={true}
          />
          <ScheduleTime
            taskData={taskData}
            isEditable={true}
          />          
          <Recurrent
            taskData={taskData}
            isEditable={true}
          />
         
          {/* Botones */}
          <Box display="flex" justifyContent="flex-end" flexDirection={{ xs: 'column', sm: 'row' }} gap={2} mt={3}>
            <Button color="error" variant="contained" onClick={handleCancelTask} fullWidth sx={{ p: 2 }}>
              Cancelar
            </Button>
            <Button color="primary" variant="contained" onClick={handleSaveTask} fullWidth sx={{ p: 2 }}>
              Guardar
            </Button>
          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}
