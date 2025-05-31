import { callExternalApi } from "../services/external-api.service";


const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;


export const getAvailableProfessional = async (prof_id) => {
  const config = {
    url: `${apiServerUrl}/available/professionals?prof_id=${encodeURIComponent(prof_id)}`,
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  };

  const { data, error } = await callExternalApi({ config });

  if (error) {
    console.error("Error al obtener datos:", error);
    throw error;
  }

  // Procesar la respuesta para agregar el campo 'type' a cada objeto, manteniendo la estructura original
  const result = {};

  for (const [key, items] of Object.entries(data)) {
    if (Array.isArray(items)) {
      result[key] = items.map((item) => ({
        ...item,
        type: key, // Agregar el campo 'type' con el nombre de la clave
      }));
    } else {
      result[key] = items;
    }
  }

  return result;
};

export const postSpecific = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: body,
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};

export const postRecurrent = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: body,
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};
