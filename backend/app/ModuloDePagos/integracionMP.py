# SDK de Mercado Pago
from os import getenv
import mercadopago


# Agrega credenciales (private key)
sdk = mercadopago.SDK(getenv("ACCESS_TOKEN_MP"))


# Crea un ítem en la preferencia (esto seria la reserva)
def getPreference():
    preference_data = {
        "items": [
            {
                "title": "Mi producto",
                "quantity": 1,
                "unit_price": 1.5,
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return preference