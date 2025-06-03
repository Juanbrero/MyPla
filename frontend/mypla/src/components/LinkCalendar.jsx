import {
    Box, Button, Typography, Modal
  } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const LinkCalendar = () => {
    const navigate = useNavigate()

    const link = () => {
      navigate('/calendar')
    };
    
    return (
        <Button
          variant="contained"
          color="primary"
          onClick={link}
          sx={{ marginTop: 2 }}
        >
          Ir a Agenda
        </Button>
    )
}