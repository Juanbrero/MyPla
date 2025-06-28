import * as React from 'react';
import { Box, Button, Typography, Modal, Checkbox, Divider } from '@mui/material';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 500,
  bgcolor: 'background.paper',
  borderRadius: '12px',
  boxShadow: 24,
  p: 4,
  color: 'text.primary',
  overflowY: 'auto',
  maxHeight: '90vh',
};

export default function SelectTipoDisponibilidadModal({
  open,
  onClose,
  onDisponibilidad,
  onEvento,
}) {
  return (
    <Modal open={open} onClose={onClose}>
        <Box sx={style}>
          <Typography variant="h5" mb={2}>
            Agregar a la agenda 
          </Typography>

          {/* Botones */}
          <Box
            display="flex"
            justifyContent="flex-end"
            flexDirection={{ xs: 'column', sm: 'column' }}
            gap={2}
          >
            <Button
              color="primary"
              variant="outlined"
              onClick={() => onDisponibilidad?.()}
              fullWidth
              sx={{ p: 2 }}
            >
              Agregar disponibilidad horaria
            </Button>
            <Button
                color="warning"
                variant="outlined"
                onClick={() => onEvento?.()}
                fullWidth
                sx={{ p: 2 }}
                >
                Crear evento
            </Button>
          </Box>
        </Box>
    </Modal>
  );
}