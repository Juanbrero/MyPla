import * as React from 'react';
import {
  Box, Button, Typography, Modal
} from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
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


export default function ScheduleCreate({
  open,
  onClose,
  taskData,
  onCancelTask,
  onSaveTask,
}) {

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

  const handleCancelTask = () => {
    onCancelTask?.(selectedTopicsState);
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

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h6" mb={2}>Editar Horario</Typography>

          <Topics 
            taskData={taskData}
            isEditable={true}
            onChangeData={handleTaskDataChange}
          />
          <ScheduleDate 
            taskData={taskData}
            isEditable={true}
            onChangeData={handleTaskDataChange}
          />
          <ScheduleTime
            taskData={taskData}
            isEditable={true}
            onChangeData={handleTaskDataChange}
          />          
          <Recurrent
            taskData={taskData}
            isEditable={true}
            onChangeData={handleTaskDataChange}
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
