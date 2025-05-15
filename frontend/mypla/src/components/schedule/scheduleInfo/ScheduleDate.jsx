import * as React from 'react';
import {
  Box, Typography, MenuItem, Select, FormControl, InputLabel
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useEffect } from 'react'

const DAYS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

export default function ScheduleDate(props) {
  const { taskData, isEditable, onChangeData} = props;

  const [day, setDay] = React.useState(taskData?.day || 'Lunes');
  const [isRecurring, setIsRecurring] = React.useState(taskData?.recurrent || false);
  const [selectedDate, setSelectedDate] = React.useState(taskData?.date ? new Date(taskData.date) : new Date());

  useEffect(() => {
    if (taskData?.day && taskData.day !== day) {
      setDay(taskData?.day || 'Lunes');
    }
    if (taskData?.date) {
      const [year, month, dayStr] = taskData.date.split("-");
      const generateDate = new Date(year, month - 1, dayStr);
      if (generateDate.toDateString() !== selectedDate.toDateString()) {
        setSelectedDate(generateDate);
      }
    } else if (!taskData?.date && selectedDate.toDateString() !== new Date().toDateString()) {
      setSelectedDate(new Date());
    }
    }, [taskData?.day, taskData?.date]);
  
  console.log("render date");
  
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
          <Typography variant="subtitle1"><strong>{isRecurring ? 'Día' : 'Fecha'}:</strong> 
            {isRecurring ? day : selectedDate.toLocaleDateString()}
          </Typography>
        </Box>  
        ) : (
          isRecurring ? (
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