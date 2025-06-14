import { Box, Typography, Divider } from '@mui/material';
import './profile.css'

export default function AdminProfile({ token, user }) {
  return (
    <Box className="profile-container" sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Perfil del Administrador
      </Typography>

      <Divider sx={{ my: 2 }} />

      <p><strong>Nombre:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
    </Box>
  );
}