import { callExternalApi } from "../external-api.service";
const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getPayPending = async (token) => {

    const config = {
    url: `${apiServerUrl}/pay-pending`,
    method: "GET",
    headers: {
        "content-type": "application/json",
        "Authorization": `Bearer ${token}`,
    }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data;
};