import React, { useEffect, useState } from "react";
import axios from "axios";
import { initMercadoPago, Wallet } from '@mercadopago/sdk-react'

// public key
initMercadoPago('poner clave');

const MPButton = () => {
  const [preferenceId, setPreferenceId] = useState(null);

  useEffect(() => {
    // Hacer una solicitud al backend para obtener el preference_id
    const getPreferenceId = async () => {
      try {
        const response = await axios.post("http://localhost:8002/create_preference");
        setPreferenceId(response.data.id); // Guardar el preference_id
      } catch (error) {
        console.error("Error al obtener el preference_id:", error);
      }
    };

    getPreferenceId();
  }, []);

  if (!preferenceId) {
    return <div>Cargando...</div>; // Muestra un cargando mientras obtenemos el preference_id
  }

  return <Wallet initialization={{ preferenceId }} />;
};

export default MPButton;