import { AlertTitle } from "@mui/material";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { Box, Tooltip } from '@mui/material';


const createOrder = import.meta.env.VITE_PP_CREATE;
const captureOrder = import.meta.env.VITE_PP_CAPTURE;
const clientID = import.meta.env.VITE_PP_CLIENT_ID;

const PayPalButton = () => {
    return (
        <PayPalScriptProvider options={{ "client-id": clientID }}>
            <Box position="relative" display="inline-block" width="100%" minHeight={48}>
                <PayPalButtons
                    disabled
                    style={{
                        layout: "horizontal", // "vertical" o "horizontal"
                        color: "gold",        // "gold" | "blue" | "silver" | "black"
                        shape: "sharp",       // "rect" | "pill" | "sharp"
                        label: "checkout",    // "paypal" | "checkout" | "buynow" | "pay"
                        tagline: false        // Mostrar o no tagline
                    }}
                    createOrder={async () => {
                        const response = await fetch(createOrder, {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ product_id: "curso_python" })
                        });
                    
                        if (!response.ok) {
                            throw new Error("Error al crear la orden");
                        }

                        const data = await response.json();
                        return data.id;
                    }}
                    
                    onApprove={async (data) => {
                        const response = await fetch(captureOrder, {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ orderID: data.orderID }),
                        });

                        if (!response.ok) {
                            throw new Error("Error al capturar el pago");
                        }
                        
                        const details = await response.json();
                        alert(`Pago realizado por ${details.payer.name.given_name}`);
                    }}
                    
                    onError={(err) => {
                        console.error("Error en el pago", err);
                    }}
                />
                {/* Overlay encima del botón */}
                <Tooltip title="Próximamente..." arrow>
                <Box
                    sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    bgcolor: 'rgba(255, 255, 255, 0.5)',
                    cursor: 'not-allowed',
                    borderRadius: 2,
                    zIndex: 10,
                    }}
                />
                </Tooltip>
            </Box>
        </PayPalScriptProvider>
    );
};

export default PayPalButton;