import * as React from 'react';
import {
  Box, Typography, TextField
} from '@mui/material';
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useEffect } from 'react'
import { dateFormater, stringDateToLocalTime, dateObjToLocalTime } from '../../../utils/dateFormater';

export default function ScheduleTime(props) {
  const { taskData, clickedEvent, isEditable, onChangeData, editando } = props;


  // const [startTime, setStartTime] = React.useState(taskData?.start ? new Date(`${taskData.date}T${taskData.start}:00`) : new Date());
  // const [endTime, setEndTime] = React.useState(taskData?.end ? new Date(`${taskData.date}T${taskData.end}:00`) : new Date());

  // const [editando, setEditando] = React.useState(clickedEvent ? true : false);
  const [startTime, setStartTime] = React.useState(editando ? (taskData ? new Date (`${taskData.start}:00`) : null) : new Date(`${taskData.date}T${taskData.start}:00`));
  const [endTime, setEndTime] = React.useState(editando ? (taskData ? new Date (`${taskData.end}:00`) : null) : new Date(`${taskData.date}T${taskData.end}:00`));
  // const [startTime, setStartTime] = React.useState(editando? taskData?.start ? new Date(`${taskData.date}T${taskData.start}:00`) : new Date(`${clickedEvent?.start}:00`));
  // const [endTime, setEndTime] = React.useState(taskData?.end ? new Date(`${taskData.date}T${taskData.end}:00`) : new Date(`${clickedEvent?.end}:00`));
  const [editStart, setEventStart] = React.useState(clickedEvent?.start);
  const [editEnd, setEventEnd] = React.useState(clickedEvent?.end);
  
  console.log("startTime: ", typeof startTime, "value: ", startTime);
  console.log("taskData.start: ", typeof taskData.start, "value: ", taskData.start);
  console.log("clickedEvent?.start: ", typeof clickedEvent?.start, "value: ", clickedEvent?.start);


  useEffect(() => {
    if (taskData?.start) {
      // setStartTime(new Date(`${taskData.date}T${taskData.start}:00`));
      setStartTime(editando ? (taskData ? new Date (`${taskData}:00`) : null) : new Date(`${taskData.date}T${taskData.start}:00`));
    } 
    // else {
    //   setStartTime(null); // o new Date() si querés un valor por defecto
    // }
  
    if (taskData?.end) {
      // setEndTime(new Date(`${taskData.date}T${taskData.end}:00`));
      setEndTime(editando ? (taskData ? new Date (`${taskData}:00`) : null) : new Date(`${taskData.date}T${taskData.end}:00`));
    }
    //  else {
    //   setEndTime(null); // o new Date()
    // }

    if (clickedEvent?.start && clickedEvent?.end) {
      setEventStart(clickedEvent.start);
      setEventEnd(clickedEvent.end);
    }

    console.log("======== en useEffect =========");
    console.log("startTime: ", typeof startTime, "value: ", startTime);
    console.log("taskData.start: ", typeof taskData.start, "value: ", taskData.start);
    console.log("clickedEvent?.start: ", typeof clickedEvent?.start, "value: ", clickedEvent?.start);

  }, [taskData?.start, taskData?.end, clickedEvent?.start, clickedEvent?.end]);
    

    // const formatTime = (date) => {
    //     if (!(date instanceof Date)) return date
    //     return date.slice(0, 5)
    // } // 'HH:MM'
    
    const handleStartChange = (newValue) => {

      if (newValue instanceof Date && !isNaN(newValue)) {
        setStartTime(newValue);
        const formattedStart = dateObjToLocalTime(newValue);
        onChangeData?.({ ...taskData, start: formattedStart });
        console.log("======== en handleStartChange.if =========");
        console.log("startTime: ", typeof startTime, "value: ", startTime);
        console.log("taskData.start: ", typeof taskData.start, "value: ", taskData.start);
        console.log("clickedEvent?.start: ", typeof clickedEvent?.start, "value: ", clickedEvent?.start);
      }
      console.log("======== en handleStartChange =========");
      console.log("startTime: ", typeof startTime, "value: ", startTime);
      console.log("taskData.start: ", typeof taskData.start, "value: ", taskData.start);
      console.log("clickedEvent?.start: ", typeof clickedEvent?.start, "value: ", clickedEvent?.start);


    };

    const handleEndChange = (newValue) => {

      if (newValue instanceof Date && !isNaN(newValue)) {
        setEndTime(newValue);
        const formattedEnd = dateObjToLocalTime(newValue);
        onChangeData?.({ ...taskData, end: formattedEnd });
        console.log("======== en handleEndChange.if =========");
        console.log("endTime: ", typeof endTime, "value: ", endTime);
        console.log("taskData.end: ", typeof taskData.end, "value: ", taskData.end);
        console.log("clickedEvent?.end: ", typeof clickedEvent?.end, "value: ", clickedEvent?.end);
      }

      console.log("======== en handleEndChange =========");
      console.log("endTime: ", typeof endTime, "value: ", endTime);
      console.log("taskData.end: ", typeof taskData.end, "value: ", taskData.end);
      console.log("clickedEvent?.end: ", typeof clickedEvent?.end, "value: ", clickedEvent?.end);

    };

    
    return (
        <>
          {!isEditable ? (
            <Box>
              <Typography variant="subtitle1">
                <strong>Horario:</strong> {dateFormater(editStart).slice(0, 5)} - {dateFormater(editEnd).slice(0, 5)}
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