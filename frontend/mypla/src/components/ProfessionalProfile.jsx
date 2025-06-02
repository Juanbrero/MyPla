import React from 'react';
import { Box, Typography, Divider } from '@mui/material';
import ProfessionalAddTopic from './ProfessionalAddTopic';
import './professionalProfile.css'

export default function ProfessionalProfile({ token }) {
  return (
    <Box className="profile-container" sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Perfil del Profesional
      </Typography>

      <Divider sx={{ my: 2 }} />

      {/* Agregar nuevos tópicos */}
      <ProfessionalAddTopic token={token} />
    </Box>
  );
}
