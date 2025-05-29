const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;
import { callExternalApi } from "../external-api.service";

export const getProfessionalsTopic = async (prof_id, token) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic?prof_id=${encodeURIComponent(prof_id)}`,
    method: "GET",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
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
        data: topics, // 🔥 Aquí devolvemos solo el array de strings
        error: null,
    };
};
