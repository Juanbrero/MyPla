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
//   start: 'HH:MM:00.000Z',
//   end: 'HH:MM:00.000Z',
//   topics: ['Matematica', 'Lengua'],
//   avaliableTopics: ['Matematica', 'Lengua', 'Programacion'],
//   day: "2025-05-31",
//   week_day: 1, (lunes)
//   recurrent: false,
//   selectedHour: 'HH:MM:00.000Z',   // para generar excepciones
// };
// mode = 'create', 'edit'

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

export default function ScheduleModal({
  open,
  onClose,
  taskData,
  mode = 'create', // 'create' o 'edit'
  // clickedEvent,    // opcional, para el modo 'edit'
  onCancelTask,
  onSaveTask,
  onDeleteTask,
  onCancelOneOccurrence,
}) {
  if (!taskData) return null;

  const [localTaskData, setLocalTaskData] = React.useState(taskData);
  const [isEditable, setIsEditable] = React.useState(mode === 'create');

  React.useEffect(() => {
    if (open) {
      setLocalTaskData(taskData);
      setIsEditable(mode === 'create'); // resetear al abrir
    }
  }, [open, taskData, mode]);

  const handleTaskDataChange = (partialUpdate) => {
    setLocalTaskData((prev) => ({
      ...prev,
      ...partialUpdate,
    }));
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

    if (mode === 'edit') {
      // Editar evento existente
      const updatedEvent = {
        ...clickedEvent,
        ...localTaskData,
      };
      onSaveTask?.(updatedEvent);
    } else {
      // Crear nuevo
      onSaveTask?.(localTaskData);
    }

    setIsEditable(false);
  };

  const handleDeleteTask = () => {
    // TODO
  }

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>
            {mode === 'edit' ? 'Información del Horario' : 'Crear Horario'}
          </Typography>

          <Topics
            value={localTaskData.topics || []}
            topicsList={localTaskData.avaliableTopics}
            onChange={(newTopics) => handleTaskDataChange({ topics: newTopics })}
            isEditable={isEditable}
          />

          <ScheduleDate
            type={localTaskData.recurrent ? 'recurrent' : 'specific'}
            value={{ week_day: localTaskData.week_day, date: localTaskData.day }}
            onChange={(newVal) => {
              if (localTaskData.recurrent) {
                handleTaskDataChange({ week_day: newVal.week_day });
              } else {
                handleTaskDataChange({ day: newVal.date });
              }
            }}
            isEditable={isEditable}
          />

          <ScheduleTime
            value={{ start: localTaskData.start, end: localTaskData.end }}
            onChange={(newTimes) => handleTaskDataChange(newTimes)}
            isEditable={isEditable}
          />

          <Recurrent
            value={localTaskData.recurrent || false}
            onChange={(newRecurrent) => {
              if (mode === 'create') {
                handleTaskDataChange({ recurrent: newRecurrent });
              }
            }}
            isEditable={mode === 'create'} // solo editable en creación
          />

          {/* Botones */}
          <Box display="flex" justifyContent="flex-end" flexDirection={{ xs: 'column', sm: 'row' }} gap={2} mt={3}>
            {!isEditable && localTaskData.recurrent === true && (
              <Button color="error" variant="contained" onClick={() => onCancelOneOccurrence} fullWidth sx={{ p: 2 }}>
                Cancelar solo por esta vez
              </Button>
            )}
            {(mode === 'create' || !isEditable) && (
              <Button color="secondary" variant="outlined" onClick={() => onCancelTask?.()} fullWidth sx={{ p: 2 }}>
                Volver
              </Button>
            )}
            {mode === 'edit' && !isEditable ? (
              <Button color="primary" variant="contained" onClick={() => setIsEditable(true)} fullWidth sx={{ p: 2 }}>
                Editar tarea
              </Button>
            ) : (
              <>
                {mode === 'edit' && (
                  <>
                    <Button color="error" variant="contained" onClick={handleDeleteTask} fullWidth sx={{ p: 2 }}>
                      Borrar tarea
                    </Button>
                    <Button color="secondary" variant="outlined" onClick={() => setIsEditable(false)} fullWidth sx={{ p: 2 }}>
                      Cancelar cambios
                    </Button>
                  </>
                )}
                <Button color="primary" variant="contained" onClick={handleSaveTask} fullWidth sx={{ p: 2 }}>
                  Guardar
                </Button>
              </>
            )}
          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}
