import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";

const PayPalButton = () => {
    return (
        <PayPalScriptProvider options={{ "client-id": "ARGUVtWZMyf9-h-k0_L_xGyODWmlP9mHvg7flo691pbKhjmuw-GjxurNkyxOJQIu48T4PedCn6uq9GZ1" }}>
            <PayPalButtons
                style={{
                    layout: "horizontal", // "vertical" o "horizontal"
                    color: "gold",        // "gold" | "blue" | "silver" | "black"
                    shape: "sharp",       // "rect" | "pill" | "sharp"
                    label: "checkout",    // "paypal" | "checkout" | "buynow" | "pay"
                    tagline: false        // Mostrar o no tagline
                  }}
                createOrder={(data, actions) => {
                    return actions.order.create({
                        purchase_units: [{
                            amount: {
                                value: "75.76", // Monto del pago
                            },
                        }],
                    });
                }}
                onApprove={(data, actions) => {
                    return actions.order.capture().then((details) => {
                        alert(`Pago realizado por ${details.payer.name.given_name}`);
                    });
                }}
                onError={(err) => {
                    console.error("Error en el pago", err);
                }}
            />
        </PayPalScriptProvider>
    );
};

export default PayPalButton;