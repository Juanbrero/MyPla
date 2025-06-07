import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getAvailableStudent = async (token, prof_id, dia) => {
  const config = {
    url: `${apiServerUrl}/available/student?prof_id=${encodeURIComponent(prof_id)}&day=${encodeURIComponent(dia)}`,
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
  }
  const { data, error } = await callExternalApi({ config })
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