import { callExternalApi } from "../external-api.service";
import { dateFormater } from "../../utils/dateFormater"
import { prof_id } from "../../utils/testData";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getSpecific = async (token) => {

    const config = {
    url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
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

export const putSpecific = async (token, newSpecific, oldSpecific) => {

    console.log("newSpecific: ", newSpecific);
    const oldStartISO = dateFormater(oldSpecific.start);
    const newStartISO = newSpecific.start ? dateFormater(newSpecific.start) : "";
    const newEndISO = newSpecific.end ? dateFormater(newSpecific.end) : "";

    const config = {
    url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
    method: "PUT",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    },
    data: {
        day     : oldSpecific.extendedProps.date,
        start   : oldStartISO,
        Nday    : newSpecific.extendedProps.date ? newSpecific.extendedProps.date : "",
        Nstart  : newStartISO,
        Nend    : newEndISO,
        topics  : newSpecific.extendedProps.eventTopics ? newSpecific.extendedProps.eventTopics : [],
    }
    };

    console.log(config);
    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const postSpecific = async (token, specific) => {

    const startISO = dateFormater(specific.start);
    const endISO = dateFormater(specific.end);

    const config = {
    url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    },
    data: {
        day     : specific.extendedProps.date,
        start   : startISO,
        end     : endISO,
        topics  : specific.extendedProps.eventTopics,
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const deleteSpecific = async (token, specific) => {
  
    const startISO = dateFormater(specific.start);

    const config = {
        url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
        method: "DELETE",
        headers: {
            "content-type": "application/json",
            // "Authorization": `Bearer ${token}`,
        },
        data: {
            day: specific.extendedProps.date,
            start: startISO,
        },
    };
    console.log("config: ", config);

    const { data, error } = await callExternalApi({ config });

    console.log("data: ", data);
    return {
        data: data,
        error,
    };
};