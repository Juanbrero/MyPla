import { Box, Button, Typography, Checkbox } from '@mui/material';
import React from 'react';
import ScheduleDate from '../../shedule/schedule-components/ScheduleDate';
import ScheduleTopics from '../../shedule/schedule-components/ScheduleTopics';

export default function SelectStep({ taskData, onClose, onChange, onNext, style}) {

    const [localTaskData, setLocalTaskData] = React.useState(taskData);
    const [selectedHour, setSelectedHour] = React.useState(null);
    
    React.useEffect(() => {
        setLocalTaskData(taskData);
    }, [taskData]);


    const handleTaskDataChange = (partialUpdate) => {
        // const updated = {
        // ...localTaskData,
        // ...partialUpdate,
        // };
        // setLocalTaskData(updated);
        // onChange?.(updated);
        setLocalTaskData(partialUpdate);
        onChange?.(partialUpdate);
    };

    const toggleSelectedHour = (hour) => {
        // const newSelected = selectedHour === hour ? null : hour;
        // setSelectedHour(newSelected);
        // handleTaskDataChange({ selectedHour: newSelected });
        const newStart = selectedHour === hour ? null : hour;
        setSelectedHour(newStart);

        if (newStart) {
            const newEnd = (parseInt(newStart.slice(0, 2), 10) + 1).toString().padStart(2, '0') + newStart.slice(2);
            onChange?.({ start: newStart, end: newEnd });
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
    }

    
    const cleanTopicsList = Array.isArray(taskData.avaliableTopics)
        ? taskData.avaliableTopics.flatMap(t => t.split(',').map(s => s.trim()))
        : [];

    const cleanSelectedTopics = Array.isArray(localTaskData.topics)
        ? localTaskData.topics.flatMap(t => t.split(',').map(s => s.trim()))
        : [];


    return (
        <Box sx={style}>
            <Typography variant="h6" mb={2}>
                Crear reserva
            </Typography>

            <ScheduleTopics
                value={cleanSelectedTopics}
                topicsList={cleanTopicsList}
                onChange={(newTopics) =>
                    handleTaskDataChange({ topics: newTopics })
                }
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