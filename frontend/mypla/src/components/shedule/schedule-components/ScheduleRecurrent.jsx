import * as React from 'react';
import {
  Box, Typography, Checkbox, FormControlLabel
} from '@mui/material';

export default function ScheduleRecurrent({ value = false, onChange, isEditable }) {
  const handleChange = (event) => {
    onChange?.(event.target.checked);
  };

  if (!isEditable) {
    return (
      <Box>
        <Typography variant="subtitle1">
          <strong>Es recurrente:</strong> {value ? 'Sí' : 'No'}
        </Typography>
      </Box>
    );
  }

  return (
    <FormControlLabel
      control={
        <Checkbox
          checked={value}
          onChange={handleChange}
        />
      }
      label="Repetir semanalmente"
      sx={{ mt: 2 }}
    />
  );
}
