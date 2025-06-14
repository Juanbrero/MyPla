import * as React from 'react';
import { 
  TextField,
  FormControl,
  InputAdornment,
  Typography
} from '@mui/material';

export default function InputPrice({ 
  value = '', 
  onChange, 
  label = 'Precio',
  currencySymbol = '$',
  placeholder = '0.00',
  error = null,
  helperText = ''
}) {

  const handleChange = (event) => {
    // Validar que solo sean números o punto decimal
    const inputValue = event.target.value;
    
    // Expresión regular que permite números con opcional punto decimal y hasta 2 decimales
    if (/^\d*\.?\d{0,2}$/.test(inputValue) || inputValue === '') {
      onChange(inputValue);
    }
  };

  return (
    <FormControl fullWidth margin="normal">
      <TextField
        label={label}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        error={error}
        helperText={helperText || (error ? "Por favor ingrese un precio válido" : "")}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              {currencySymbol}
            </InputAdornment>
          ),
          inputMode: 'decimal', // Muestra teclado numérico en dispositivos móviles
        }}
        // Asegura que el tipo sea 'text' para manejar el punto decimal correctamente
        type="text"
      />
    </FormControl>
  );
}