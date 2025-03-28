# SDK de Mercado Pago
import mercadopago


# Agrega credenciales (private key)
sdk = mercadopago.SDK("poner clave")


# Crea un ítem en la preferencia (esto seria la reserva)

preference_data = {
    "items": [
        {
            "id": "111",
            "category_id": "",
            "currency_id": "ARS",
            "description": "abc",
            "title": "Mi producto",
            "quantity": 1,
            "unit_price": 75.76,
        }
    ]
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
print(preference)

def getPreference():
    global preference
    return preference