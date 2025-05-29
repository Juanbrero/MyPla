import { callExternalApi } from "../external-api.service";
import { dateFormater } from "../../utils/dateFormater"

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const postSpecific = async (prof_id, token, specific) => {

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

    console.log(config);

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

// export const getSpecific = async (prof_id, token, specific) => {

//     const startISO = dateFormater(specific.start);
//     const endISO = dateFormater(specific.end);

//     const config = {
//     url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
//     method: "GET",
//     headers: {
//         "content-type": "application/json",
//         // "Authorization": `Bearer ${token}`,
//     }
//     };

//     const { data, error } = await callExternalApi({ config });

//     return {
//         data: data,
//         error,
//     };
// };