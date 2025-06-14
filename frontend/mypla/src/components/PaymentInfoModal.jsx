import { Box, Modal, Typography, Divider, Button } from '@mui/material';
import ReceiptIcon from '@mui/icons-material/Receipt';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import LabelIcon from '@mui/icons-material/Label';
import PersonIcon from '@mui/icons-material/Person';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import { getProfessional } from '../services/professionals/professionals.service';
import { useEffect, useState } from 'react';


const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 520,
  bgcolor: 'background.paper',
  borderRadius: 3,
  boxShadow: 24,
  p: 4,
  color: 'text.primary',
  overflowY: 'auto',
  maxHeight: '90vh',
  fontFamily: 'Roboto, sans-serif',
};

const itemStyle = {
  display: 'flex',
  alignItems: 'center',
  mb: 2,
};

const iconStyle = {
  mr: 1.5,
  color: 'primary.main',
};


export default function PaymentInfoModal({ open, onClose, paymentRow }) {
  
  const { id, address, alum, prof, prof_id, concept, amount, date } = paymentRow;

  const getComision = async ()=> {
    const PORCENTAJE_COMISION = 0.1;
    const profFind = await getProfessional(prof_id);
    const PUNTAJE_PROF = parseFloat(profFind.data.score);
    const INDICE_VALORACION = 0.05 - (PUNTAJE_PROF/100);
    setComFinal(PORCENTAJE_COMISION + INDICE_VALORACION);
  }

  const [com_final, setComFinal] = useState(0);

  
  useEffect(() => {
    getComision();
  },[paymentRow]);

  if (!paymentRow) return null;
  

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography
          variant="h5"
          fontWeight={700}
          color="primary.main"
          textAlign="center"
          mb={3}
        >
          Datos de la operación
        </Typography>

        <Box sx={itemStyle}>
          <ReceiptIcon sx={iconStyle} />
          <Typography variant="body1">
            <strong>ID #:</strong> {id}
          </Typography>
        </Box>

        <Box sx={itemStyle}>
          <CalendarTodayIcon sx={iconStyle} />
          <Typography variant="body1">
            <strong>Fecha:</strong> {date}
          </Typography>
        </Box>

        <Box sx={itemStyle}>
          <LabelIcon sx={iconStyle} />
          <Typography variant="body1" component="span">
            <strong>Concepto:</strong>{' '}
            <Box
              component="span"
              sx={{
                color: concept === 'Reembolso' ? 'error.main' : 'success.main',
                fontWeight: 600,
              }}
            >
              {concept}
            </Box>
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={itemStyle}>
          <PersonIcon sx={iconStyle} />
          <Typography variant="body1">
            <strong>Alumno:</strong> {alum}
          </Typography>
        </Box>

        <Box sx={itemStyle}>
          <PersonIcon sx={iconStyle} />
          <Typography variant="body1">
            <strong>Profesional:</strong> {prof}
          </Typography>
        </Box>

        <Box sx={itemStyle}>
          <AccountBalanceIcon sx={iconStyle} />
          <Typography variant="body1">
            <strong>CBU/CVU:</strong> {address}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={itemStyle}>
          <MonetizationOnIcon sx={iconStyle} />
          <Typography variant="body1" fontWeight={600}>
            <strong>Monto Bruto:</strong> $ {amount}
          </Typography>
        </Box>
        {concept === 'Reserva' &&
          <Box sx={itemStyle}>
            <MonetizationOnIcon sx={iconStyle} />
            <Typography variant="body1" fontWeight={600}>
              <strong>Monto Final a Pagar (comisiones aplicadas):</strong> $ {(parseFloat(amount) * (1 - com_final)).toFixed(2)}
            </Typography>
          </Box>
        }

        {/* Botón centrado para cerrar */}
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={onClose}
            sx={{
              borderRadius: 3,
              px: 4,
              py: 1.5,
              fontWeight: 600,
              boxShadow: '0 4px 10px rgba(25, 118, 210, 0.3)',
              textTransform: 'none',
              '&:hover': {
                boxShadow: '0 6px 14px rgba(25, 118, 210, 0.5)',
              },
            }}
          >
            Cerrar
          </Button>
        </Box>

      </Box>

    </Modal>
  );
}
