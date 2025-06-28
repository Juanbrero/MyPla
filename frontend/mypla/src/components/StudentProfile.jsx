import { Box, Typography, Divider } from '@mui/material';
import './profile.css'
import { useNavigate } from "react-router-dom";


export default function StudentProfile({ token, user }) {
  
  ///////////////////////////////////////////
  const navigate = useNavigate();
  ///////////////////////////////////////////
  
  
  return (
    <Box className="profile-container" sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Bienvenido: <strong>{user.nickname}</strong>
      </Typography>
      <Typography variant="p" gutterBottom>Tipo de usuario: <strong>Alumno</strong></Typography>

      <Divider sx={{ my: 2 }} />

      <button onClick={() => navigate('/califications/pending')}>Clases pendientes de calificacion</button>

    </Box>
  );
}
