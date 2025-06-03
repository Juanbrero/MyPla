import React, { useEffect, useState } from "react";
import axios from "axios";
import { initMercadoPago, Wallet } from '@mercadopago/sdk-react'

const pkey = import.meta.env.VITE_MP_TOKEN;
const preferenceResponse = import.meta.env.VITE_MP_PREFERENCE;

initMercadoPago(pkey);

const MPButton = () => {
  const [preferenceId, setPreferenceId] = useState(null);

  useEffect(() => {
    // Hacer una solicitud al backend para obtener el preference_id
    const getPreferenceId = async () => {
      try {
        const response = await axios.post(preferenceResponse);
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