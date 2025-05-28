import * as React from 'react';
import {
  Box, Button, Typography, Modal
} from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { es } from 'date-fns/locale'; // Español opcional
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


export default function ScheduleEdit({
  open,
  clickedEvent,
  onClose,
  taskData,
  onCancelTask,
  onSaveEditTask,
  onDeleteTask,
  onCancelOneOccurrence,
}) {

  const [isEditable, setIsEditable] = React.useState(false); // Controla si el formulario es editable
  const [localTaskData, setLocalTaskData] = React.useState(taskData);

  React.useEffect(() => {
    if (open) setLocalTaskData(taskData);
  }, [open, taskData]);
  
  const handleTaskDataChange = (partialUpdate) => {
       
    setLocalTaskData((prev) => ({
      ...prev,
      ...partialUpdate,
    }));
  };
  
  const handleCancelOneOccurrence = () => {

    onCancelOneOccurrence?.(clickedEvent);
  };

  const handleDeleteTask = () => {
    onDeleteTask?.(clickedEvent);
    setIsEditable(false);
  };

  const handleSaveEditTask = () => {

    const { topics, start, end } = localTaskData;
    
    if (!topics?.length || !start || !end) {
      alert('Por favor complete todos los campos');
      return;
    }
    
    if (start >= end) {
      alert('La hora de inicio no puede ser mayor o igual que la de fin');
      return;
    }

    let dateStr;

    if (typeof localTaskData.date === "string") {
      dateStr = localTaskData.date;
    } else if (localTaskData.date instanceof Date) {
      const y = localTaskData.date.getFullYear();
      const m = String(localTaskData.date.getMonth() + 1).padStart(2, '0');
      const d = String(localTaskData.date.getDate()).padStart(2, '0');
      dateStr = `${y}-${m}-${d}`;
    }

    console.log(dateStr);
    console.log(localTaskData.day);

    const editEvent = {
      ...clickedEvent,
      color     :     localTaskData.recurrent ? 'green' : 'orange', 
      start     :     `${dateStr}T${localTaskData.start}`,
      end       :     `${dateStr}T${localTaskData.end}`,
      extendedProps : {
        day         : localTaskData.day,
        date        : dateStr,
        recurrent   : localTaskData.recurrent,
        eventTopics : localTaskData.topics,
      },
    }
    
    console.log("clickedEvent: ", clickedEvent);
    console.log("editEvent: ", editEvent);

    setIsEditable(false); // Regresar al modo de solo lectura después de guardar
    onSaveEditTask?.(editEvent);
    
  };

  const handleCancelChanges = () => {
    setIsEditable(false); // Regresar al modo de solo lectura
  };

  const handleEditSchedule = () => {
    setIsEditable(true); // Permite editar el horario
  };


  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>Información del Horario</Typography>
          <Topics 
            taskData={localTaskData}
            clickedEvent={clickedEvent}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />
          <ScheduleDate 
            taskData={localTaskData}
            clickedEvent={clickedEvent}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />
          <ScheduleTime
            taskData={taskData}
            clickedEvent={clickedEvent}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />
          <Recurrent
            taskData={localTaskData}
            clickedEvent={clickedEvent}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />

          {/* Botones */}
          <Box display="flex" justifyContent="flex-end" flexDirection={{ xs: 'column', sm: 'row' }} gap={2} mt={3}>
            {!isEditable ? (
              <>
                {clickedEvent.extendedProps.recurrent && (
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
                <Button color="primary" variant="contained" onClick={handleSaveEditTask} fullWidth sx={{ p: 2 }}>
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
