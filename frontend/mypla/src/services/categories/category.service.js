import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getCategories = async () => {

    const config = {
    url: `${apiServerUrl}/category`,
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