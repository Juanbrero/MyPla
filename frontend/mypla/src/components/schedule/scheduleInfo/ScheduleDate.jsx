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

    // actualizaciones sobre taskData
    if (taskData?.day && taskData?.date) {
      let year, month, dayStr;
      
      // actualizo date
      // formateo manual la date a yyyy-mm-dd
      if (typeof taskData.date === "string") {
        [year, month, dayStr] = taskData.date.split("-");
      } else if (taskData.date instanceof Date) {
        year = taskData.date.getFullYear();
        month = String(taskData.date.getMonth() + 1).padStart(2, '0');
        dayStr = String(taskData.date.getDate()).padStart(2, '0');
      }
      const generateDate = new Date(year, month - 1, dayStr);
      
      if (generateDate.toDateString() !== selectedDate.toDateString()) {
        setSelectedDate(generateDate);
      }
      else if (!taskData?.date && selectedDate !== new Date()) {
        setSelectedDate(new Date());
      }
      
      // actualizo day
      if (taskData.day !== day) {
        setDay(taskData.day);
      }
      else {
        setDay(clickedEvent?.extendedProps?.day);
      }

    }

    // actualizaciones sobre clickedEvent
    if(clickedEvent?.extendedProps?.date && clickedEvent?.extendedProps?.day) {
      const [eventYear, eventMonth, eventDay] = clickedEvent.extendedProps.date.split("-");
      const generateEventDate = new Date(eventYear, eventMonth - 1, eventDay);
      setEditDate(generateEventDate);
      setEditDay(clickedEvent.extendedProps.day);
    }

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