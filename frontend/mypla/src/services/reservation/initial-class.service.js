import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const initialClass = async (token, taskData, prof_id) => {

    console.log(taskData)
    const body = {
        day_hour: `${taskData.day}T${taskData.start}`,
        prof_id: prof_id,
        topic: taskData.topics[0]
    }

    const config = {
        url: `${apiServerUrl}/reservation/start-class`,
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        data: body
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};