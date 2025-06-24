import { callExternalApi } from "../external-api.service";
const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getEvents = async (page, amount) => {

    const config = {
        url: `${apiServerUrl}/event?page=${page}&amount=${amount}`,
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

export const postEvents = async (token, body) => {

    const config = {
        url: `${apiServerUrl}/event`,
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        data: body,
    };

    const { data, error } = await callExternalApi({ config });

    
    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data;
};