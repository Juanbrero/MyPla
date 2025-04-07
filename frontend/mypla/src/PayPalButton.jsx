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
                createOrder={async () => {
                    const response = await fetch("http://localhost:8002/create-order", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ product_id: "curso_python" })
                    });
                
                    const data = await response.json();
                    return data.id;
                }}
                
                onApprove={async (data) => {
                    const response = await fetch(`http://localhost:8002/capture-order`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ orderID: data.orderID }),
                    });
                    const details = await response.json();
                    alert(`Pago realizado por ${details.payer.name.given_name}`);
                }}
                
                onError={(err) => {
                    console.error("Error en el pago", err);
                }}
            />
        </PayPalScriptProvider>
    );
};

export default PayPalButton;