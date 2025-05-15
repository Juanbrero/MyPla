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
  onClose,
  taskData,
  onCancelTask,
  onSaveTask,
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
    onCancelOneOccurrence?.(taskData);
  };

  const handleDeleteTask = () => {
    onDeleteTask?.(taskData);
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
    setIsEditable(false); // Regresar al modo de solo lectura después de guardar
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
            taskData={taskData}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />
          <ScheduleDate 
            taskData={taskData}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />
          <ScheduleTime
            taskData={taskData}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />
          <Recurrent
            taskData={taskData}
            isEditable={isEditable}
            onChangeData={handleTaskDataChange}
          />

          {/* Botones */}
          <Box display="flex" justifyContent="flex-end" flexDirection={{ xs: 'column', sm: 'row' }} gap={2} mt={3}>
            {!isEditable ? (
              <>
                {taskData?.recurrent && (
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
