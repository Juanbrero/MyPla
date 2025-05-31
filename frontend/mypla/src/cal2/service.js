import { callExternalApi } from "../services/external-api.service";


const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;


export const getAvailableProfessional = async (prof_id) => {
  const config = {
    url: `${apiServerUrl}/available/professionals?prof_id=${encodeURIComponent(prof_id)}`,
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      // "Authorization": `Bearer ${token}`, // Si usás autenticación
    },
  };

  const { data, error } = await callExternalApi({ config });

  if (error) {
    console.error("Error al obtener datos:", error);
    throw error;
  }

  return data;
};