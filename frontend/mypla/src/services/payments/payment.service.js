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

export const putPayPending = async (token, body) => {

    const config = {
        url: `${apiServerUrl}/pay-finished`,
        method: "PUT",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        data: {
            body:body,
        }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data;
};

export const putRefundPending = async (token, body) => {

    const config = {
        url: `${apiServerUrl}/pay-refund`,
        method: "PUT",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        data: {
            body:body,
        }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data;
};