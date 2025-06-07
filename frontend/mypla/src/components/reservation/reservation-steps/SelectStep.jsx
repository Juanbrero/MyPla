import { Box, Button, Typography, Checkbox } from '@mui/material';
import React from 'react';
import ScheduleDate from '../../shedule/schedule-components/ScheduleDate';
import ScheduleTopicsReservation from '../ScheduleTopicsReservation';

export default function SelectStep({ taskData, onClose, onChange, onNext, style }) {

  const [localTaskData, setLocalTaskData] = React.useState(taskData);
  const [selectedHour, setSelectedHour] = React.useState(taskData.start);

  React.useEffect(() => {
    setLocalTaskData(taskData);
  }, [taskData]);

  // Inicializar tópico si no hay ninguno seleccionado
    React.useEffect(() => {
        if (
            (!taskData.topics || taskData.topics.length === 0) &&
            Array.isArray(taskData.avaliableTopics) &&
            taskData.avaliableTopics.length > 0
        ) {
            const firstTopic = taskData.avaliableTopics[0];
            const update = { topics: [firstTopic], selectedTopic: firstTopic };
            setLocalTaskData(prev => ({ ...prev, ...update }));
            onChange?.(update);
        }
    }, [taskData.avaliableTopics]);


    const handleTaskDataChange = (partialUpdate) => {
        const update = {
            ...partialUpdate,
            ...(partialUpdate.topics?.[0] ? { selectedTopic: partialUpdate.topics[0] } : {}),
        };
        setLocalTaskData(prev => ({ ...prev, ...update }));
        onChange?.(update);
    };

  const toggleSelectedHour = (hour) => {
    if (selectedHour !== hour) {
      setSelectedHour(hour);
      const newEnd = (parseInt(hour.slice(0, 2), 10) + 1).toString().padStart(2, '0') + hour.slice(2);
      onChange?.({ start: hour, end: newEnd });
    }
  };

  const getHourRange = (start, end) => {
    const startHour = parseInt(start.slice(0, 2), 10);
    const endHour = parseInt(end.slice(0, 2), 10);
    const suffix = start.slice(2);
    const hours = [];
    for (let h = startHour; h < endHour; h++) {
      hours.push(h.toString().padStart(2, '0') + suffix);
    }
    return hours;
  };

  const topicsList = Array.isArray(taskData.topics)
    ? taskData.topics
    : [];

  const selectedTopic = Array.isArray(localTaskData.topics)
    ? localTaskData.topics[0] || ''
    : '';

  return (
    <Box sx={style}>
      <Typography variant="h6" mb={2}>
        Crear reserva
      </Typography>

      <ScheduleTopicsReservation
        value={selectedTopic}
        topicsList={topicsList}
        onChange={(newTopic) => handleTaskDataChange({ topics: [newTopic] })}
        isEditable={true}
      />

      <ScheduleDate
        type={'specific'}
        value={{ week_day: taskData?.week_day, date: taskData?.day }}
        isEditable={false}
      />

      <Box mt={2}>
        <Typography variant="subtitle1" mb={1}>
          <strong>Selecciona el horario de tu reserva:</strong>
        </Typography>
        {getHourRange(taskData.start, taskData.end).map((hour) => (
          <Box key={hour} display="flex" alignItems="center" mb={1}>
            <Checkbox
              checked={selectedHour === hour}
              onChange={() => toggleSelectedHour(hour)}
            />
            <Typography ml={1}>{hour.slice(0, 5)}</Typography>
          </Box>
        ))}
      </Box>

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
          onClick={onNext}
          fullWidth
          sx={{ p: 2 }}
        >
          Aceptar
        </Button>
      </Box>
    </Box>
  );
}
