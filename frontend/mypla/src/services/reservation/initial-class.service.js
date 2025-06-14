import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const initialClass = async (token, taskData, prof_id) => {

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

export const getStudentReservations = async (token) => {

    const config = {
    url: `${apiServerUrl}/reservation/student`,
    method: "GET",
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

export const cancelStudentReservations = async (token, day_hour, user_id) => {
    const config = {
    url: `${apiServerUrl}/reservation/cancel?day_hour=${encodeURIComponent(day_hour)}&user_id=${encodeURIComponent(user_id)}`,
    method: "PUT",
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