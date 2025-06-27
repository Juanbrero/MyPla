import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;


export const getInvites = async (token) => {

    const config = {
    url: `${apiServerUrl}/event/invite`,
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

export const patchInvite = async (token, body) => {

    const config = {
        url: `${apiServerUrl}/event/invite`,
        method: "PATCH",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        data: body,
    
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};