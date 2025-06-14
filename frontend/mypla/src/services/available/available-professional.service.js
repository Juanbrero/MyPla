import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

function sumarUnaHora(horaStr) {
  let [hh, mm, ss] = horaStr.split(":").map(Number);
  hh = (hh + 1) % 24; // Sumar 1 y controlar que no pase de 23
  return `${hh.toString().padStart(2, "0")}:${mm.toString().padStart(2, "0")}:${ss.toString().padStart(2, "0")}`;
}


export const getAvailableProfessional = async (token) => {
  const config = {
    url: `${apiServerUrl}/available/professionals`,
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
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
      result[key] = items.map((item) => (key === 'class_' ? {
        ...item,
        type: key, 
        day: item.day_hour.split("T")[0],
        start: item.day_hour.split("T")[1],
        end: sumarUnaHora(item.day_hour.split("T")[1]),
        topics: [item.topics],
      } : {
        ...item,
        type: key,
      }));
    } else {
      result[key] = items;
    }
  }

  return result;
};