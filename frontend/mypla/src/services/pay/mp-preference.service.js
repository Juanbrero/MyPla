import { callExternalApi } from "../external-api.service";
const preferenceResponse = import.meta.env.VITE_MP_PREFERENCE;

export const mpPreference = async (token) => {

    const config = {
    url: preferenceResponse,
    method: "POST",
    headers: {
        "Authorization": `Bearer ${token}`,
    }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data
};