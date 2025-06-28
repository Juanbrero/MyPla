
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

export default function VerEventoModal({
  open,
  onClose,
  taskData,
  onDeleteEvento,
}) {
  if (!taskData) return null;
  else console.log(taskData)
 

  const handleDeleteEvent = () => {
    onClose?.()   
  };

  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h5" mb={2}>
            Evento "{taskData.title || ''}"
          </Typography>

        <>

            <ScheduleDate
                type={'specific'}
                value={{ week_day: 1, date: taskData.day }}
                isEditable={false}
            />

            <ScheduleTime
                value={{ start:taskData.start, end:taskData.end }}
                isEditable={false}
            />

            <ScheduleTopicsReservation
                value={taskData.topic || ''}
                isEditable={false}
            />

            <Typography>Precio: ${taskData.precio}</Typography>

            
            {taskData.invitados && (
                <Typography fontWeight="bold" mb={1}>Invitados:</Typography> &&
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {taskData.invitados.map((invitado) => (
                        <Chip
                        key={invitado.topic_name}
                        label={`${invitado.topic_name} - $${invitado.price_class}`}
                        onClick={() => handleOpenModal(invitado)}
                        sx={{
                            // backgroundColor: '#1cb698',
                            color: '#fff',
                            fontWeight: 500,
                        }}
                        />
                    ))}
                </Box>
            )}
            
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
                color="error"
                variant="contained"
                onClick={handleDeleteEvent}
                fullWidth
                sx={{ p: 2 }}
            >
                Cancelar evento
            </Button>        

          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}