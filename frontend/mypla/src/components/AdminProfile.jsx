import { Box, Typography, Divider } from '@mui/material';
import './profile.css'

export default function AdminProfile({ token, user }) {
  return (
    <Box className="profile-container" sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Bienvenido: <strong>{user.nickname}</strong>
      </Typography>
      <Typography variant="p" gutterBottom>Tipo de usuario: <strong>Administrador</strong></Typography>

      <Divider sx={{ my: 2 }} />
    </Box>
  );
}