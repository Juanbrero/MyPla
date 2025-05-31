import * as React from 'react';
import {
  Box, Typography, MenuItem, Select, FormControl, InputLabel
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useEffect } from 'react';
import { DateTime } from 'luxon';

const DAYS = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

export default function ScheduleDate(props) {
  const { taskData, clickedEvent, isEditable, onChangeData } = props;

  const [day, setDay] = React.useState('Lunes');
  const [selectedDate, setSelectedDate] = React.useState(new Date());

  // Actualizo estados cuando cambia taskData o clickedEvent
  useEffect(() => {
    if (!clickedEvent?.extendedProps) return;

    const { type, day: dayStr, day_hour, week_day } = clickedEvent.extendedProps;

    if (type === 'recurrent') {
      if (typeof week_day === 'number') {
        setDay(DAYS[week_day]);
      }
    } else {
      let dateVal = null;

      if (type === 'specific' || type === 'exception') {
        dateVal = dayStr;
      } else if (type === 'class_') {
        dateVal = day_hour;
      }

      if (dateVal) {
        const dateObj = new Date(dateVal);
        if (!isNaN(dateObj)) {
          setSelectedDate(dateObj);
        }
      }
    }
  }, [clickedEvent]);

  const handleDayChange = (event) => {
    const { value } = event.target;
    setDay(value);
    const dayIndex = DAYS.indexOf(value);
    onChangeData?.({ week_day: dayIndex });
  };

  const handleDateChange = (newValue) => {
    setSelectedDate(newValue);
    onChangeData?.({ date: newValue });
  };

  return (
    <>
      {!isEditable ? (
        <Box>
          <Typography variant="subtitle1">
            <strong>{clickedEvent?.extendedProps?.type === 'recurrent' ? 'Día' : 'Fecha'}: </strong>
            {clickedEvent?.extendedProps?.type === 'recurrent'
              ? day
              : selectedDate.toLocaleDateString()}
          </Typography>
        </Box>
      ) : (
        clickedEvent?.extendedProps?.type === 'recurrent' ? (
          <FormControl fullWidth margin="normal">
            <InputLabel>Día</InputLabel>
            <Select
              value={day}
              onChange={handleDayChange}
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
  );
}
