const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;
import { callExternalApi } from "../external-api.service";

export const getProfessionalTopics = async (token) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic`,
    method: "GET",
    headers: {
        "content-type": "application/json",
        "Authorization": `Bearer ${token}`,
    }
    };

    const { data, error } = await callExternalApi({ config });

    console.log(data)
    console.log(error)

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    const topics = Array.isArray(data)
        ? data.map(item => item.topic_name)
        : [];


    return topics;
};

export const postProfessionalTopics = async (token, topic) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic`,
    method: "POST",
    headers: {
        "content-type": "application/json",
        "Authorization": `Bearer ${token}`,
    },
    data: {
        topic_name: topic,
        price_class: 1.1,
    },
    };

    console.log(config)
    
    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};
