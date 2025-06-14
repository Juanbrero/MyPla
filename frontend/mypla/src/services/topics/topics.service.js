import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getTopics = async () => {

    const config = {
    url: `${apiServerUrl}/topics`,
    method: "GET",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const postTopic = async (topic) => {

    const config = {
    url: `${apiServerUrl}/topics?topic_name=${topic}`,
    method: "POST",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};