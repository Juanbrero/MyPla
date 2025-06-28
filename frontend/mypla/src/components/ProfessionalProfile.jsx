import React from 'react';
import { Box, Typography, Divider } from '@mui/material';
import ProfessionalAddTopic from './ProfessionalAddTopic';
import './profile.css'

export default function ProfessionalProfile({ token, user }) {
  return (
    <Box className="profile-container" sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Bienvenido: <strong>{user.nickname}</strong>
      </Typography>
      <Typography variant="p" gutterBottom>Tipo de usuario: <strong>Profesional</strong></Typography>

      <Divider sx={{ my: 2 }} />

      {/* Agregar nuevos tópicos */}
      <ProfessionalAddTopic token={token} />

    </Box>
  );
}
