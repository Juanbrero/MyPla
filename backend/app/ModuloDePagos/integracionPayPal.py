from os import getenv
import requests

PAYPAL_CLIENT_ID = getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = getenv("PAYPAL_SECRET")
PAYPAL_API_URL = "https://api-m.sandbox.paypal.com"  # Cambia a producción cuando sea necesario

# Obtener el token de PayPal
def get_paypal_token():
    auth_response = requests.post(
        f"{PAYPAL_API_URL}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )
    return auth_response.json().get("access_token")

# Crear una orden de pago
def create_order(amount="10.00", currency="USD"):
    access_token = get_paypal_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": currency, "value": amount}}],
    }
    response = requests.post(f"{PAYPAL_API_URL}/v2/checkout/orders", json=order_data, headers=headers)
    return response.json()

# Capturar un pago
def capture_order(order_id):
    access_token = get_paypal_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{PAYPAL_API_URL}/v2/checkout/orders/{order_id}/capture", headers=headers)
    return response.json()

# Ejemplo de uso
if __name__ == "__main__":
    order = create_order()
    print("Orden creada:", order)

    # Simulación: el usuario paga y devuelve un orderID
    order_id = order.get("id")
    if order_id:
        payment = capture_order(order_id)
        print("Pago capturado:", payment)
