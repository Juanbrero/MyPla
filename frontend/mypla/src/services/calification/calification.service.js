import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;


export const getCalificate = async (token) => {

    const config = {
    url: `${apiServerUrl}/calificate`,
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


export const patchCalification = async (token, body) => {

    const config = {
        url: `${apiServerUrl}/calificate/student`,
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