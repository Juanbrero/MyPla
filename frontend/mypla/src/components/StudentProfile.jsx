import { Box, Typography, Divider } from '@mui/material';
import './profile.css'
import { useNavigate } from "react-router-dom";


export default function StudentProfile({ token, user }) {
  
  ///////////////////////////////////////////
  const navigate = useNavigate();
  ///////////////////////////////////////////
  
  
  return (
    <Box className="profile-container" sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Perfil del Alumno
      </Typography>

      <Divider sx={{ my: 2 }} />

      <p><strong>Nombre:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>

      <button onClick={() => navigate('/califications/pending')}>Clases pendientes de calificacion</button>

    </Box>
  );
}
