import { Modal } from '@mui/material';
import { useEffect, useState } from 'react';
import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { StarsGrid } from './StarsGrid';


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

export default function CalificationModal({
  open,
  onClose,
//   token,
//   prof_id
}) {

    useEffect(() => {
        if (!open) {
            setRating(0);
            setHoverRating(0);
        }
    }, [open]);

    const [rating, setRating] = useState(0);
    const [hoverRating, setHoverRating] = useState(0);

    const handleSelectStar = (index) => {
        setRating(index); // índice 1 a 5
    };

    const handleHover = (index) => {
        setHoverRating(index);
    };

    const handleLeave = () => {
        setHoverRating(0);
    };

    const handleSubmit = () => {
        console.log("Calificación enviada:", rating);
        
        onClose?.();
    };


    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={style}>
                <Typography variant="h6" mb={2}>
                    Califica tu experiencia!
                </Typography>

                <StarsGrid
                    rating={rating}
                    hoverRating={hoverRating}
                    onSelectEvent={handleSelectStar}
                    onHover={handleHover}
                    onLeave={handleLeave}
                />


                {/* Botones */}
                <Box
                    display="flex"
                    justifyContent="flex-end"
                    flexDirection={{ xs: 'column', sm: 'row' }}
                    gap={2}
                    mt={3}
                >       
                    <Button
                        color="primary"
                        variant="contained"
                        onClick={handleSubmit}
                        fullWidth
                        sx={{ p: 2 }}
                    >
                        Enviar
                    </Button>
                </Box>
            </Box>
            
        </Modal>
    )

}