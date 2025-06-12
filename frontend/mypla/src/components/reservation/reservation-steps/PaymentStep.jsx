import { Box, Button, Typography, Modal } from '@mui/material';
import PayPalButton from '../paymentButtons/PayPalButton';
import MPButton from '../paymentButtons/MPButton';


export default function PaymentStep({ onClose, onNext, style, reservationInfo, token}) {

    console.log(reservationInfo);

    // guardar reservationInfo en bd con una tabla temporal


    return (    
        <Box sx={style}>
            <Typography variant="h6" mb={2}>
                Seleccionar medio de pago
            </Typography>

            <Box>
            
                <div className='paypalButton'>
                    <PayPalButton fullWidth></PayPalButton>
                    
                </div>
            </Box>
            <Box>
                <div className="mpButton">
                    <MPButton fullWidth token={token}></MPButton> 
                </div>
            
            </Box>

            <Box
                display="flex"
                justifyContent="flex-end"
                flexDirection={{ xs: 'column', sm: 'row' }}
                gap={2}
                mt={3}
                paddingTop={10}
            >       
                <Button
                    color="secondary"
                    variant="outlined"
                    onClick={onNext}
                    // onClick={() => onClose?.()}
                    fullWidth
                    sx={{ p: 2 }}
                >
                    Cancelar
                </Button>

            </Box>

        </Box>
    );

}