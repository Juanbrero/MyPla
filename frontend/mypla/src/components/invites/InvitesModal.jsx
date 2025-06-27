import { Modal } from '@mui/material';
import { useEffect, useState } from 'react';
import React from 'react';
import { Box, Typography, Button } from '@mui/material';


// const style = {
//   position: 'absolute',
//   top: '50%',
//   left: '50%',
//   transform: 'translate(-50%, -50%)',
//   width: '90%',
//   maxWidth: 500,
//   bgcolor: 'background.paper',
//   borderRadius: '12px',
//   boxShadow: 24,
//   p: 4,
//   color: 'text.primary',
//   overflowY: 'auto',
//   maxHeight: '90vh',
// };
const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 500,
  bgcolor: '#fff',
  borderRadius: '12px',
  boxShadow: 24,
  p: 4,
  color: '#333',
  overflowY: 'auto',
  maxHeight: '90vh',
  fontFamily: 'Segoe UI, sans-serif',
  lineHeight: 1.6,
};


export default function InvitesModal({
  open,
  onClose,
  token,
  event,
}) {


    const handleSubmit = async (isAccepted) => {
        
        const body = {
            prof_id: event.prof_id,
            day_hour: event.day_hour,
            accept: isAccepted,
        }
        await patchInvite(token, body);
        onClose?.();
    };

    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={style}>
                {/* Título */}
                <Typography variant="h5" component="h2" gutterBottom mb={2} textAlign={'center'}>
                    ¡Te invitaron a formar parte de este evento!
                </Typography>

                {/* Cuadro de remitente */}
                <Box sx={{
                    bgcolor: '#f1f1f1',
                    border: '1px solid #ddd',
                    borderRadius: 1,
                    px: 2,
                    py: 1,
                    mb: 2,
                    fontSize: 14,
                    color: '#555'
                }}>
                    De: <strong>{event.professional_username}</strong>
                </Box>

                {/* Cuerpo del mensaje */}
                <Box sx={{
                    bgcolor: '#f9f9f9',
                    p: 2,
                    borderRadius: 2,
                    border: '1px solid #ddd',
                    mb: 3
                }}>
                    <Typography variant="body1" component="div">
                        <p>Hola,</p>
                        <p>
                            Me gustaría que seas parte del staff en mi evento <strong>{event.title}</strong>,
                            a realizarse el día <strong>{event.date}</strong> a las <strong>{event.hour}hs</strong>.
                        </p>
                        <p>
                            El mismo tendrá una duración de <strong>{event.duration}hs</strong>.
                        </p>
                        <p>¡Espero tu respuesta! :)</p>
                    </Typography>
                </Box>

                {/* Botones de acción */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
                    <Button variant="outlined" color="error" fullWidth onClick={() => handleSubmit(false)}>
                        Rechazar invitación
                    </Button>
                    <Button variant="contained" color="success" fullWidth onClick={() => handleSubmit(true)}>
                        Aceptar invitación
                    </Button>
                </Box>

            </Box>
            
        </Modal>
    )

}