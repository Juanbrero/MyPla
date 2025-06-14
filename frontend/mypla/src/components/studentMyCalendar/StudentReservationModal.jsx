import * as React from 'react';
import { Box, Button, Typography, Modal, Checkbox, Divider } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { es } from 'date-fns/locale';
import ScheduleTopics from '../shedule/schedule-components/ScheduleTopics';
import ScheduleDate from '../shedule/schedule-components/ScheduleDate';
import ScheduleTime from '../shedule/schedule-components/ScheduleTime';

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

export default function StudentReservationModal({
  open,
  onClose,
  taskData,
  onDeleteTask,
}) {
  if (!taskData) return null;
  const [localTaskData, setLocalTaskData] = React.useState(taskData);

  React.useEffect(() => {
    if (open) {
      setLocalTaskData(taskData);
    }
  }, [open, taskData]);


  // BORRAR
  const handleDeleteReservation = () => {
    onDeleteTask?.(taskData);
    onClose?.()
  }


  return (
    <Modal open={open} onClose={onClose}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
        <Box sx={style}>
          <Typography variant="h5" mb={2}>
            Reserva
          </Typography>

          <Typography variant="h6" mb={2}>
            Clase con: {localTaskData.prof_username}
          </Typography>
        <>
            <ScheduleTopics
                value={localTaskData.topics || []}
                topicsList={localTaskData.avaliableTopics}
                isEditable={false}
            />

            <ScheduleDate
                type={'specific'}
                value={{ week_day: 1, date: localTaskData.day }}
                isEditable={false}
            />

            <ScheduleTime
                value={{ start: localTaskData.start, end: localTaskData.end }}
                isEditable={false}
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
                color="error"
                variant="contained"
                onClick={handleDeleteReservation}
                fullWidth
                sx={{ p: 2 }}
                >
                Cancelar reserva
            </Button>
          </Box>
        </Box>
      </LocalizationProvider>
    </Modal>
  );
}