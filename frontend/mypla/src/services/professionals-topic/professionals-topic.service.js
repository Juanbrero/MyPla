const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;
import { callExternalApi } from "../external-api.service";
import { prof_id } from "../../utils/testData";

export const getProfessionalTopics = async (prof_id) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic?prof_id=${encodeURIComponent(prof_id)}`,
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

    const topics = Array.isArray(data)
        ? data.map(item => item.topic_name)
        : [];


    return topics;
};

export const postProfessionalTopics = async (topic) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
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
