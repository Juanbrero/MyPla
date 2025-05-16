import * as React from 'react';
import {
  Box, Typography, TextField
} from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers';
import { useEffect } from 'react'

export default function ScheduleTime(props) {
  const { taskData, isEditable, onChangeData } = props;

  const [startTime, setStartTime] = React.useState(taskData?.start ? new Date(`1970-01-01T${taskData.start}:00`) : null);
  const [endTime, setEndTime] = React.useState(taskData?.end ? new Date(`1970-01-01T${taskData.end}:00`) : null);

  useEffect(() => {
    if (taskData?.start) {
      setStartTime(new Date(`1970-01-01T${taskData.start}:00`));
    } else {
      setStartTime(null); // o new Date() si querés un valor por defecto
    }
  
    if (taskData?.end) {
      setEndTime(new Date(`1970-01-01T${taskData.end}:00`));
    } else {
      setEndTime(null); // o new Date()
    }
  }, [taskData?.start, taskData?.end]);
    


    const formatTime = (date) => {
        if (!(date instanceof Date)) return date
        return date.toTimeString().slice(0, 5)
    } // 'HH:MM'
    
    const handleStartChange = (newValue) => {
      console.log("nuevs start: " + formatTime(newValue));
      setStartTime(newValue);
      onChangeData?.({ start : formatTime(newValue)});
    };

    const handleEndChange = (newValue) => {
      setEndTime(newValue);
      onChangeData?.({ end : formatTime(newValue)});
    };

    return (
        <>
          {!isEditable ? (
            <Box>
              <Typography variant="subtitle1"><strong>Horario:</strong> {formatTime(startTime)} - {formatTime(endTime)}</Typography>
            </Box>
          ) : (
            <Box display="flex" gap={2} mt={2} flexDirection={{ xs: 'column', sm: 'row' }}>
              <TimePicker
                label="Inicio"
                value={startTime}
                onChange={handleStartChange}
                minutesStep={30}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
              <TimePicker
                label="Fin"
                value={endTime}
                onChange={handleEndChange}
                minutesStep={30}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </Box>
          )}
        </>
    )

}