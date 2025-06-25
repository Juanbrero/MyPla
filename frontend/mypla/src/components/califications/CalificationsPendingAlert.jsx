import { Modal } from '@mui/material';
import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from "react-router-dom";


const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 500,
  bgcolor: 'background.paper',
  borderRadius: '12px',
  boxShadow: 24,
  p: 4,
  color: 'text.primary',
  overflowY: 'auto',
  maxHeight: '90vh',
};

export default function CalificationsPendingAlert({
  open,
  onClose,
  token,
}) {

    const navigate = useNavigate();

    const handleSubmit = () => {
        
        navigate('/califications/pending');
        onClose?.();
    };


    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={style}>
                <Typography variant="h5" mb={5} textAlign={'center'}>
                    <strong>Tenes clases sin calificar!</strong>
                </Typography>
    
                 <Button
                    color="primary"
                    variant="contained"
                    onClick={handleSubmit}
                    fullWidth
                    sx={{ p: 2, mb:2 }}
                    
                >
                    Ir
                </Button>
                <Button
                    color="error"
                    variant="outlined"
                    onClick={() => onClose?.()}
                    fullWidth
                    sx={{ p: 2 }}
                >
                    Cerrar
                </Button>
                
            </Box>
            
        </Modal>
    )

}