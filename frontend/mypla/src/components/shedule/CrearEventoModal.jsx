import * as React from 'react';
import { Box, Button, Typography, Modal, TextField, InputAdornment, Autocomplete } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { es } from 'date-fns/locale';
import ScheduleDate from './schedule-components/ScheduleDate';
import ScheduleTime from './schedule-components/ScheduleTime';
import ScheduleTopicsReservation from '../reservation/ScheduleTopicsReservation'

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

export default function CrearEventoModal({
  open,
  onClose,
  taskData,
  onSaveEvento,
}) {
  if (!taskData) return null;
 
  const [localTaskData, setLocalTaskData] = React.useState(taskData);
 
  React.useEffect(() => {
    if (open) {
      setLocalTaskData(taskData);
    }
  }, [open, taskData]);


    const handleTaskDataChange = (partialUpdate) => {
        console.log(partialUpdate)
    setLocalTaskData((prev) => ({
      ...prev,
      ...partialUpdate,
    }));
  };

  const handleSaveTask = () => {
    const { selectedTopic, start, end, precio, nombre } = localTaskData;
    localTaskData.idsProfesionales = localTaskData.selectedProfessors?.map(p => p.prof_id) || [];
    
    if (!selectedTopic?.length || !start || !end || !precio || !nombre) {
      alert('Por favor complete todos los campos');
      return;
    }
    if (start >= end) {
      alert('La hora de inicio no puede ser mayor o igual que la de fin');
      return;
    }
    onSaveEvento?.(localTaskData);
    onClose?.()   
  };

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h5" mb={2}>
            Crear Evento
          </Typography>

        <>

            <TextField
                mt={2}
                id="outlined-basic"
                label="Nombre"
                variant="outlined"
                fullWidth
                margin="normal"
                value={localTaskData.nombre || ''}
                onChange={(e) => handleTaskDataChange({ nombre: e.target.value })}
            />

            <ScheduleDate
                type={'specific'}
                value={{ week_day: 1, date: localTaskData.day }}
                isEditable={true}
                onChange={(newVal) => 
                    handleTaskDataChange({ day: newVal.date })}
            />

            <ScheduleTime
                value={{ start: localTaskData.start, end: localTaskData.end }}
                onChange={(newTimes) => handleTaskDataChange(newTimes)}
                isEditable={true}
            />

            <ScheduleTopicsReservation
                value={localTaskData.selectedTopic || ''}
                topicsList={localTaskData.avaliableTopics || []}
                isEditable={true}
                onChange={(newVal) => 
                    handleTaskDataChange({ selectedTopic: newVal })}
            />

            <TextField
                mt={2}
                margin="normal"
                label="Precio"
                type="number"
                inputProps={{ min: 0, step: 100 }}
                InputProps={{
                    startAdornment: <InputAdornment position="start">$</InputAdornment>,
                }}
                fullWidth
                value={localTaskData.precio || ''}
                onChange={(e) => handleTaskDataChange({ precio: e.target.value })}
            />

            <Autocomplete
                multiple
                options={taskData.professors || []}
                getOptionLabel={(option) => option.prof_username}
                isOptionEqualToValue={(option, value) => option.prof_id === value.prof_id}
                value={localTaskData.selectedProfessors || []}
                onChange={(event, newValue) =>
                    handleTaskDataChange({ selectedProfessors: newValue })
                }
                renderInput={(params) => (
                    <TextField
                    {...params}
                    label="Invitados"
                    placeholder="Selecciona profesionales"
                    margin="normal"
                    />
                )}
                fullWidth
            />
        </>

          {/* Botones */}
          <Box
            display="flex"
            justifyContent="flex-end"
            flexDirection={{ xs: 'column', sm: 'row' }}
            gap={2}
            mt={3}
          >

            <Button
                color="secondary"
                variant="outlined"
                onClick={() => onClose?.()}
                fullWidth
                sx={{ p: 2 }}
            >
                Volver
            </Button>

            <Button
                color="primary"
                variant="contained"
                onClick={handleSaveTask}
                fullWidth
                sx={{ p: 2 }}
            >
                Guardar
            </Button>        

          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}