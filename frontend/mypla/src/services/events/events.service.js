import { callExternalApi } from "../external-api.service";
const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getEvents = async () => {

    const config = {
        url: `${apiServerUrl}/event`,
        method: "GET",
        headers: {
            "content-type": "application/json",
        }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data;
};