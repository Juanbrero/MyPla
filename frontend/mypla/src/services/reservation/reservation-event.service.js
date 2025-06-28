import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const postReservationEvent = async (token, event, prof_id) => {
    console.log(token)

    const body = {
        day_hour: `${event.day_hour}`,
        prof_id: prof_id,
        topic: event.topic,
    }
    const config = {
        url: `${apiServerUrl}/reservation/start-event`,
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
