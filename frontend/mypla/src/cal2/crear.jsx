import * as React from 'react';
import { Box, Button, Typography, Modal } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { es } from 'date-fns/locale';
import Topics from './schedule/scheduleInfo/Topics';
import ScheduleDate from './schedule/scheduleInfo/ScheduleDate';
import ScheduleTime from './schedule/scheduleInfo/ScheduleTime';
import Recurrent from './schedule/scheduleInfo/Recurrent';


// RECIBE Y DEVUELVE:

// taskData = {
//   start: `HH:MM:00.000Z`,
//   end: `HH:MM:00.000Z`,
//   topics: ['Matematica', 'Lengua'],
//   avaliableTopics: ['Matematica', 'Lengua', 'Programacion'],
//   day: "2025-05-31",
//   week_day: 1, (lunes)
//   recurrent: false,
// };


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

export default function ScheduleCreate({
  open,
  onClose,
  taskData,
  onCancelTask,
  onSaveTask,
}) {

  if (!taskData) return null;

  const [localTaskData, setLocalTaskData] = React.useState(taskData);

  React.useEffect(() => {
    if (open) setLocalTaskData(taskData);
    console.log(localTaskData)
  }, [open, taskData]);

  const handleTaskDataChange = (partialUpdate) => {
    setLocalTaskData((prev) => ({
      ...prev,
      ...partialUpdate,
    }));
  };

  const handleCancelTask = () => {
    onCancelTask?.(localTaskData);
  };

  const handleSaveTask = () => {
    const { topics, start, end } = localTaskData;
    if (!topics?.length || !start || !end) {
      alert('Por favor complete todos los campos');
      return;
    }
    if (start >= end) {
      alert('La hora de inicio no puede ser mayor o igual que la de fin');
      return;
    }
    onSaveTask?.(localTaskData);
  };

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>Crear Horario</Typography>

          <Topics
            value={localTaskData.topics || []}
            topicsList={localTaskData.avaliableTopics}
            onChange={(newTopics) => handleTaskDataChange({ topics: newTopics })}
            isEditable={true}
          />

          <ScheduleDate
            type={localTaskData.recurrent ? 'recurrent' : 'specific'}
            value={{ week_day: localTaskData.week_day, date: localTaskData.day }}
            onChange={(newVal) => {
              // newVal puede tener { week_day } o { date }
              if (localTaskData.recurrent) {
                handleTaskDataChange({ week_day: newVal.week_day });
              } else {
                handleTaskDataChange({ day: newVal.date });
              }
            }}
            isEditable={true}
          />

          <ScheduleTime
            value={{ start: localTaskData.start, end: localTaskData.end }}
            onChange={(newTimes) => handleTaskDataChange(newTimes)}
            isEditable={true}
          />

          <Recurrent
            value={localTaskData.recurrent || false}
            onChange={(newRecurrent) => handleTaskDataChange({ recurrent: newRecurrent })}
            isEditable={true}
          />

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
