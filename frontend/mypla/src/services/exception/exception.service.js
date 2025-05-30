import { callExternalApi } from "../external-api.service";
import { dateFormater } from "../../utils/dateFormater"
import { prof_id } from "../../utils/testData";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getException = async (token) => {

    const config = {
    url: `${apiServerUrl}/exception?prof_id=${encodeURIComponent(prof_id)}`,
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

export const putException = async (token, newException, oldException) => {

    const oldStartISO = dateFormater(oldException.start);
    const newStartISO = newException.start ? dateFormater(newException.start) : "";
    const newEndISO = newException.end ? dateFormater(newException.end) : "";

    const config = {
    url: `${apiServerUrl}/exception?prof_id=${encodeURIComponent(prof_id)}`,
    method: "PUT",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    },
    data: {
        day     : oldException.extendedProps.date,
        start   : oldStartISO,
        Nday    : newException.extendedProps.day ? newException.extendedProps.day : "",
        Nstart  : newStartISO,
        Nend    : newEndISO,
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const postException = async (token, exception) => {

    const startISO = dateFormater(exception.start);
    const endISO = dateFormater(exception.end);

    const config = {
    url: `${apiServerUrl}/exception?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    },
    data: {
        day     : exception.extendedProps.date,
        start   : startISO,
        end     : endISO,
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const deleteException = async (token, exception) => {
  
    const startISO = dateFormater(exception.start);

    const config = {
        url: `${apiServerUrl}/exception?prof_id=${encodeURIComponent(prof_id)}`,
        method: "DELETE",
        headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
        },
        data: {
        day: exception.extendedProps.date,
        start: startISO,
        },
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};