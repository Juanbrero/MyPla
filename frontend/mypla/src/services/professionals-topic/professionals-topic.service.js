const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;
import { callExternalApi } from "../external-api.service";

export const getProfessionalsTopic = async (token) => {

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
        return { data: null, error };
    }

    const topics = Array.isArray(data)
        ? data.map(item => item.topic_name)
        : [];


    return {
        data: topics,
        error: null,
    };
};
