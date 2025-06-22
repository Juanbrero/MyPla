import React, { useState } from 'react';
import { Box, Typography, Divider } from '@mui/material';
import './profile.css'
import CalificationModal from './califications/CalificationModal';

export default function ProfessionalProfile({ token, user }) {
  
  ///////////////////////////////////////////
  
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null); 
  
  const handleCloseModal = () => {
      setModalOpen(false);
      setModalData(null);
  };
  ///////////////////////////////////////////
  
  
  return (
    <Box className="profile-container" sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Perfil del Alumno
      </Typography>

      <Divider sx={{ my: 2 }} />

      <p><strong>Nombre:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>

      <button onClick={() => setModalOpen(true)}>probar modal de calificacion</button>


      <CalificationModal
        open={modalOpen}
        onClose={handleCloseModal}
      />

    </Box>
  );
}
