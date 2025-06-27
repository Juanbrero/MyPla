import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getTopics = async () => {

    const config = {
    url: `${apiServerUrl}/topics`,
    method: "GET",
    headers: {
        "content-type": "application/json",
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const getTopicsByCategory = async (category) => {

    const config = {
    url: `${apiServerUrl}/topics/category?category_name=${category}`,
    method: "GET",
    headers: {
        "content-type": "application/json",
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const postTopic = async (body) => {
    
    const config = {
        url: `${apiServerUrl}/topics`,
        method: "POST",
        headers: {
            "content-type": "application/json",
            // "Authorization": `Bearer ${token}`,
        },
        data: {
            topic_name: body.topic_name,
            category_name: body.category_name,
        },
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};