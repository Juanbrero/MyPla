import * as React from 'react';
import { Box, Button, Typography, Modal, Checkbox } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { es } from 'date-fns/locale';
import ScheduleTopics from './schedule-components/ScheduleTopics';
import ScheduleDate from './schedule-components/ScheduleDate';
import ScheduleTime from './schedule-components/ScheduleTime';
import ScheduleRecurrent from './schedule-components/ScheduleRecurrent';


// RECIBE Y DEVUELVE:

// taskData = {
//   start: 'HH:MM:00.000Z',
//   end: 'HH:MM:00.000Z',
//   topics: ['Matematica', 'Lengua'],
//   avaliableTopics: ['Matematica', 'Lengua', 'Programacion'],
//   day: "2025-05-31",
//   week_day: 1, (lunes)
//   recurrent: false,
//   selectedHour: 'HH:MM:00.000Z', (para excepciones)  SOLO EN MODO EDITAR
//   tipo: 'recurrent', 'specific', 'exception'         SOLO EN MODO EDITAR
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
  overflowY: 'auto',
  maxHeight: '90vh',
};

function getHourRange(start, end) {
  const startHour = parseInt(start.slice(0, 2), 10);
  const endHour = parseInt(end.slice(0, 2), 10);

  const suffix = start.slice(2);
  const hours = [];
  for (let h = startHour; h < endHour; h++) {
    hours.push(h.toString().padStart(2, '0') + suffix);
  }
  return hours;
}

function agruparHorasContiguas(_horas) {
  const suffix = _horas[0].slice(2)
  let horas = []
  _horas.forEach(hora => {
    horas.push(parseInt(hora.slice(0, 2), 10))
  });
  horas.sort((a, b) => a - b);
  let res = []
  res.push({start: horas[0], end: horas[0] + 1})
  horas.shift()
  while (horas.length > 0) {
    if (res[res.length-1].end === horas[0]) {
      res[res.length-1].end += 1
    }
    else {
      res.push({start: horas[0], end: horas[0] + 1})
    }
    horas.shift()
  }
  let formattedRes = []
  res.forEach(hora => {
    formattedRes.push({start: `${hora.start.toString().padStart(2, '0') + suffix}`, end: `${hora.end.toString().padStart(2, '0') + suffix}`})
  });
  return formattedRes
}

export default function ScheduleModal({
  open,
  onClose,
  taskData,
  onSaveTask,
  onEditTask,
  onDeleteTask,
  onCreateException,
  onDeleteException,
  mode = 'create', // 'create' o 'edit'
}) {
  if (!taskData) return null;

  const [localTaskData, setLocalTaskData] = React.useState(taskData);
  const [isEditable, setIsEditable] = React.useState(mode === 'create');

  const [isSelectingExceptions, setIsSelectingExceptions] = React.useState(false);
  const [selectedHoursToCancel, setSelectedHoursToCancel] = React.useState([]);

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

  const handleCancelarCambios = () => {
    setLocalTaskData(taskData)
    setIsEditable(false)
  }

  const toggleSelectedHour = (hour) => {
    setSelectedHoursToCancel((prev) =>
      prev.includes(hour)
        ? prev.filter((h) => h !== hour)  // quitar
        : [...prev, hour]                 // agregar
    );
  };


  // CREAR y EDITAR
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
      onEditTask?.(taskData, localTaskData);
      setIsEditable(false);
    } else if (mode === 'create') {
      // Crear nuevo
      onSaveTask?.(localTaskData);
      onClose?.()
    }

  };

  // BORRAR
  const handleDeleteTask = () => {
    onDeleteTask?.(taskData);
    onClose?.()
  }

  // GENERAR EXCEPCION
  const handleCreateException = () => {
    agruparHorasContiguas(selectedHoursToCancel).forEach(excepcion => {
      let ex = {day: taskData.day, start: excepcion.start, end: excepcion.end}
      onCreateException?.(ex)
    });
    onClose?.()
  }

  const handleDeleteException = () => {
    onDeleteException?.(taskData)
    onClose?.()
  }

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>
            {mode === 'edit'
              ? 'Información del Horario'
              : mode === 'crear'
              ? 'Crear Horario'
              : 'Excepción'}
          </Typography>

          {!isSelectingExceptions && (
            <>
              {(mode === 'edit' || mode === 'create') && (
                <ScheduleTopics
                  value={localTaskData.topics || []}
                  topicsList={localTaskData.avaliableTopics}
                  onChange={(newTopics) =>
                    handleTaskDataChange({ topics: newTopics })
                  }
                  isEditable={isEditable}
                />
              )}

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

              {(mode === 'edit' || mode === 'create') && (
                <ScheduleRecurrent
                  value={localTaskData.recurrent || false}
                  onChange={(newRecurrent) => {
                    if (mode === 'create') {
                      handleTaskDataChange({ recurrent: newRecurrent });
                    }
                  }}
                  isEditable={mode === 'create'}
                />
              )}
            </>
          )}
          {/* Vista para seleccionar excepciones */}
          {isSelectingExceptions && (
            <Box mt={2}>
              <Typography variant="subtitle1" mb={1}>
                Seleccioná los horarios a cancelar:
              </Typography>
              {getHourRange(taskData.start, taskData.end).map((hour) => (
                <Box key={hour} display="flex" alignItems="center" mb={1}>
                  <Checkbox
                    checked={selectedHoursToCancel.includes(hour)}
                    onChange={() => toggleSelectedHour(hour)}
                  />
                  <Typography ml={1}>{hour.slice(0, 5)}</Typography>
                </Box>
              ))}
            </Box>
          )}

          {/* Botones */}
          <Box
            display="flex"
            justifyContent="flex-end"
            flexDirection={{ xs: 'column', sm: 'row' }}
            gap={2}
            mt={3}
          >
            {!isSelectingExceptions && (mode === 'create' || !isEditable) && (
              <Button
                color="secondary"
                variant="outlined"
                onClick={() => onClose?.()}
                fullWidth
                sx={{ p: 2 }}
              >
                Volver
              </Button>
            )}

            {!isSelectingExceptions && localTaskData.recurrent === true && !isEditable && (
              <Button
                color="warning"
                variant="contained"
                onClick={() => setIsSelectingExceptions(true)}
                fullWidth
                sx={{ p: 2 }}
              >
                Cancelar solo por esta vez
              </Button>
            )}

            {!isSelectingExceptions && mode === 'edit' && !isEditable ? (
              <Button
                color="primary"
                variant="contained"
                onClick={() => setIsEditable(true)}
                fullWidth
                sx={{ p: 2 }}
              >
                Editar tarea
              </Button>
            ) : (
              !isSelectingExceptions && (
                <>
                  {mode === 'edit' && (
                    <>
                      <Button
                        color="secondary"
                        variant="outlined"
                        onClick={handleCancelarCambios}
                        fullWidth
                        sx={{ p: 2 }}
                      >
                        Cancelar cambios
                      </Button>
                      <Button
                        color="error"
                        variant="contained"
                        onClick={handleDeleteTask}
                        fullWidth
                        sx={{ p: 2 }}
                      >
                        Borrar tarea
                      </Button>
                    </>
                  )}
                  {(mode === 'edit' || mode === 'create') && (
                    <Button
                      color="primary"
                      variant="contained"
                      onClick={handleSaveTask}
                      fullWidth
                      sx={{ p: 2 }}
                    >
                      Guardar
                    </Button>
                  )}
                  {mode === 'exception' && !isEditable && (
                    <Button
                      color="warning"
                      variant="contained"
                      onClick={handleDeleteException}
                      fullWidth
                      sx={{ p: 2 }}
                    >
                      Cancelar Excepción
                    </Button>
                  )}
                </>
              )
            )}

            {isSelectingExceptions && (
              <>
                <Button
                  variant="outlined"
                  color='secondary'
                  onClick={() => {
                    setIsSelectingExceptions(false);
                    setSelectedHoursToCancel([]);
                  }}
                  fullWidth
                  sx={{ p: 2 }}
                >
                  Deshacer
                </Button>
                <Button
                  variant="contained"
                  color="warning"
                  onClick={handleCreateException}
                  fullWidth
                  sx={{ p: 2 }}
                >
                  Confirmar cancelaciones
                </Button>
              </>
            )}
          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}
