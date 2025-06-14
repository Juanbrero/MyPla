import { callExternalApi } from "../external-api.service";
const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getProfessionalTopics = async (token, price = false) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic`,
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

    if (price) return data

    const topics = Array.isArray(data)
        ? data.map(item => item.topic_name)
        : [];


    return topics;
};

// traigo todos los profesionales de un topico
export const getProfessionalsByTopic = async (token, topicName) => {


    const config = {
    url: `${apiServerUrl}/professionals-topic/topics?topic_name=${encodeURIComponent(topicName)}`,
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


export const postProfessionalTopics = async (token, topic, price_class = 1.1) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic`,
    method: "POST",
    headers: {
        "content-type": "application/json",
        "Authorization": `Bearer ${token}`,
    },
    data: {
        topic_name: topic,
        price_class,
    },
    };
    
    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const deleteProfessionalTopics = async (token, topic) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic?topic=${encodeURIComponent(topic)}`,
    method: "DELETE",
    headers: {
        "content-type": "application/json",
        "Authorization": `Bearer ${token}`,
    }
    };
    
    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const putProfesionalTopics = async (token, topic) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic`,
    method: "PUT",
    headers: {
        "content-type": "application/json",
        "Authorization": `Bearer ${token}`,
    },
    data: topic
    };
    
    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};