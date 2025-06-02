import { callExternalApi } from "../services/external-api.service";


const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;


export const getAvailableProfessional = async (token) => {
  const config = {
    url: `${apiServerUrl}/available/professionals`,
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      'Authorization': 'Bearer ' + token
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

export const postSpecific = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/specific`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'Authorization': 'Bearer ' + token
    },
    data: body,
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};

export const postRecurrent = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'Authorization': 'Bearer ' + token
    },
    data: body,
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};

export const deleteSpecific = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/specific`,
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      'Authorization': 'Bearer ' + token
    },
    data: body,
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};


export const deleteRecurrent = async (token, week_day, start) => {
  const config = {
    url: `${apiServerUrl}/recurrent?week_day=${encodeURIComponent(week_day)}&start=${encodeURIComponent(start)}`,
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      'Authorization': 'Bearer ' + token
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};
