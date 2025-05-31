import * as React from 'react';
import {
  Box, Typography, TextField
} from '@mui/material';
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useEffect } from 'react'
import { dateFormater } from '../../../utils/dateFormater';

export default function ScheduleTime(props) {
  const { taskData, clickedEvent, isEditable, onChangeData } = props;

  const [startTime, setStartTime] = React.useState(taskData?.start ? new Date(`${taskData.date}T${taskData.start}:00`) : null);
  const [endTime, setEndTime] = React.useState(taskData?.end ? new Date(`${taskData.date}T${taskData.end}:00`) : null);
  const [editStart, setEventStart] = React.useState(clickedEvent?.start);
  const [editEnd, setEventEnd] = React.useState(clickedEvent?.end);


  useEffect(() => {
    if (taskData?.start) {
      setStartTime(new Date(`${taskData.date}T${taskData.start}:00`));
    } 
    else {
      setStartTime(null); // o new Date() si querés un valor por defecto
    }
  
    if (taskData?.end) {
      setEndTime(new Date(`${taskData.date}T${taskData.end}:00`));
    } else {
      setEndTime(null); // o new Date()
    }

    if (clickedEvent?.start && clickedEvent?.end) {
      setEventStart(clickedEvent.start);
      setEventEnd(clickedEvent.end);
    }

  }, [taskData?.start, taskData?.end, clickedEvent?.start, clickedEvent?.end]);
    

    const formatTime = (date) => {
        if (!(date instanceof Date)) return date
        return date.slice(0, 5)
    } // 'HH:MM'
    
    const handleStartChange = (newValue) => {
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
              <Typography variant="subtitle1">
                <strong>Horario:</strong> {dateFormater(editStart).slice(0, 5)} - {dateFormater(editEnd).slice(0, 5)}
                {/* <strong>Horario:</strong> {formatTime(editStart)} - {formatTime(editEnd)} */}
              </Typography>
            </Box>
          ) : (
            <Box display="flex" gap={2} mt={2} flexDirection={{ xs: 'column', sm: 'row' }}>
              <TimePicker
                label="Inicio"
                value={startTime}
                onChange={handleStartChange}
                minutesStep={30}
                ampm={false}
                inputFormat="HH:mm"
                onError={() => {}}
                renderInput={(params) => <TextField 
                                            {...params} fullWidth 
                                            onKeyDown={(e) => {
                                            e.stopPropagation(); // evita el rebote en el foco del input
                                            }}
                                        />}
              />
              <TimePicker
                label="Fin"
                value={endTime}
                onChange={handleEndChange}
                minutesStep={30}
                ampm={false}
                inputFormat="HH:mm"
                onError={() => {}}
                renderInput={(params) => <TextField 
                                            {...params} fullWidth
                                            onKeyDown={(e) => {
                                            e.stopPropagation(); // evita el rebote en el foco del input
                                            }}
                                          />}
              />
            </Box>
          )}
        </>
    )

}