import * as React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  IconButton,
  Typography,
  Box,
  InputAdornment
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

export default function ModalProfile({
  open = false,
  onClose,
  topic = '',
  currentPrice = '',
  onSave,
  onDelete
}) {
  const [price, setPrice] = React.useState(currentPrice);
  const [error, setError] = React.useState(false);

  React.useEffect(() => {
    setPrice(currentPrice);
  }, [currentPrice]);

  const handlePriceChange = (e) => {
    const value = e.target.value;
    // Validación para números y máximo 2 decimales
    if (/^\d*\.?\d{0,2}$/.test(value) || value === '') {
      setPrice(value);
      setError(false);
    }
  };

  const handleSave = () => {
    if (price === '' || isNaN(parseFloat(price))) {
      setError(true);
      return;
    }
    onSave({
        topic_name: topic,
        price_class: parseFloat(price)
    });
    onClose();
  };

  const handleDelete = () => {
    onDelete();
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Editar precio</Typography>
          <IconButton 
            onClick={handleDelete}
            color="error"
            aria-label="eliminar tópico"
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent>
        <Typography variant="subtitle1" gutterBottom>
          Tópico: <strong>{topic}</strong>
        </Typography>
        
        <TextField
          fullWidth
          margin="normal"
          label="Nuevo precio"
          value={price}
          onChange={handlePriceChange}
          error={error}
          helperText={error ? "Ingrese un precio válido" : ""}
          InputProps={{
            startAdornment: <InputAdornment position="start">$</InputAdornment>,
            inputMode: 'decimal'
          }}
          autoFocus
        />
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button 
          onClick={handleSave} 
          variant="contained" 
          color="primary"
          disabled={error || price === ''}
        >
          Guardar
        </Button>
      </DialogActions>
    </Dialog>
  );
}