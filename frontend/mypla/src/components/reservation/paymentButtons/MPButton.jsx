import React, { useEffect, useState } from "react";
import axios from "axios";
import { initMercadoPago, Wallet } from '@mercadopago/sdk-react'
import { mpPreference } from "../../../services/pay/mp-preference.service";

const pkey = import.meta.env.VITE_MP_TOKEN;
//const preferenceResponse = import.meta.env.VITE_MP_PREFERENCE;

initMercadoPago(pkey);

const MPButton = ({token}) => {
  const [preferenceId, setPreferenceId] = useState(null);

  // ir a buscar la data de la reserva a la bd

  useEffect(() => {
    // Hacer una solicitud al backend para obtener el preference_id
    const getPreferenceId = async () => {
      try {
        const response = await mpPreference(token);
        setPreferenceId(response.id); // Guardar el preference_id
      } catch (error) {
        console.error("Error al obtener el preference_id:", error);
      }
    };

    getPreferenceId();
  }, [token]);

  if (!preferenceId) {
    return <div>Cargando...</div>; // Muestra un cargando mientras obtenemos el preference_id
  }

  return <Wallet initialization={{ preferenceId }} />;
};

export default MPButton;