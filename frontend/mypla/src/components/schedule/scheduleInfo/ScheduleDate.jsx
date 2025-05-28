import * as React from 'react';
import {
  Box, Typography, MenuItem, Select, FormControl, InputLabel
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useEffect } from 'react'
import { DateTime } from "luxon";

const DAYS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

export default function ScheduleDate(props) {
  const { taskData, clickedEvent, isEditable, onChangeData} = props;

  const [day, setDay] = React.useState(taskData?.day || 'Lunes');
  const [selectedDate, setSelectedDate] = React.useState(taskData?.date ? new Date(taskData.date) : new Date());
  const [editDate, setEditDate] = React.useState(new Date(clickedEvent?.extendedProps?.date));
  const [editDay, setEditDay] = React.useState(clickedEvent?.extendedProps?.day);

  useEffect(() => {
    // if (taskData?.day && taskData.day !== day) {
    //   setDay(taskData?.day);
    // }
    // if (taskData?.date) {
    //   // const [year, month, dayStr] = taskData.date.split("-");
    //   // const generateDate = new Date(year, month - 1, dayStr);
    //   const generateDate = new Date(taskData.date);
    //   if (generateDate.toDateString() !== selectedDate.toDateString()) {
    //     setSelectedDate(generateDate);
    //   }
    // } else if (!taskData?.date && selectedDate.toDateString() !== new Date().toDateString()) {
    //   setSelectedDate(new Date());
    // }
    if (taskData?.day && taskData?.date) {
      setDay(taskData?.day);
      const generateDate = new Date(taskData.date);
      if (generateDate.toDateString() !== selectedDate.toDateString()) {
        setSelectedDate(generateDate);
      }
      else if (!taskData?.date && selectedDate.toDateString() !== new Date().toDateString()) {
       setSelectedDate(new Date());
     }
    }

    if(clickedEvent?.extendedProps?.date && clickedEvent?.extendedProps?.day) {
      const [eventYear, eventMonth, eventDay] = clickedEvent.extendedProps.date.split("-");
      const generateEventDate = new Date(eventYear, eventMonth - 1, eventDay);
      setEditDate(generateEventDate);
      setEditDay(clickedEvent.extendedProps.day);
    }
    
    // if(clickedEvent?.extendedProps?.day) {
    //   setEditDay(clickedEvent.extendedProps.day);
    // }

  }, [taskData?.day, taskData?.date, clickedEvent?.extendedProps?.date, clickedEvent?.extendedProps?.day]);
  

  const handleDayChange = (event) => {
    const { target: {value} } = event;
    setDay(value);
    onChangeData?.({ day : value});
  };

  const handleDateChange = (newValue) => {
    setSelectedDate(newValue);
    onChangeData?.({ date : newValue});
  };


  return (
    <>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1">
            <strong>{clickedEvent?.extendedProps?.recurrent ? 'Día' : 'Fecha'}: </strong> 
            {clickedEvent?.extendedProps?.recurrent ? editDay : editDate.toLocaleDateString()}
          </Typography>
        </Box>  
        ) : (
          clickedEvent?.extendedProps?.recurrent ? (
            <FormControl fullWidth margin="normal">
              <InputLabel>Día</InputLabel>
              <Select
                value={day}
                onChange= {handleDayChange}
                label="Día"
              >
                {DAYS.map((d) => (
                  <MenuItem key={d} value={d}>{d}</MenuItem>
                ))}
              </Select>
            </FormControl>
          ) : (
            <DatePicker
              label="Fecha"
              value={selectedDate}
              onChange={handleDateChange}
              slotProps={{ textField: { fullWidth: true, margin: 'normal' } }}
            />
          )
        )}
    </>
  )

}