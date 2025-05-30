import { callExternalApi } from "../external-api.service";
import { dateFormater } from "../../utils/dateFormater"
import { prof_id } from "../../utils/testData";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;
const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

export const getRecurrent = async (token) => {

    const config = {
    url: `${apiServerUrl}/recurrent?prof_id=${encodeURIComponent(prof_id)}`,
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

export const putRecurrent = async (token, newRecurrent, oldRecurrent) => {

    const oldStartISO = dateFormater(oldRecurrent.start);
    const newStartISO = newRecurrent.start ? dateFormater(newRecurrent.start) : "";
    const newEndISO = newRecurrent.end ? dateFormater(newRecurrent.end) : "";
    const indice = dias.indexOf(oldRecurrent.extendedProps.day)
    const week_day_index = indice == 0 ? 7 : indice

    const config = {
    url: `${apiServerUrl}/recurrent?prof_id=${encodeURIComponent(prof_id)}`,
    method: "PUT",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    },
    data: {
        week_day: week_day_index,
        start   : oldStartISO,
        Nstart  : newStartISO,
        Nend    : newEndISO,
        topics  : newRecurrent.extendedProps.eventTopics ? newRecurrent.extendedProps.eventTopics : [],
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const postRecurrent = async (token, recurrent) => {

    const startISO = dateFormater(recurrent.start);
    const endISO = dateFormater(recurrent.end);

    const indice = dias.indexOf(oldRecurrent.extendedProps.day)
    const week_day_index = indice == 0 ? 7 : indice

    const config = {
    url: `${apiServerUrl}/recurrent?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    },
    data: {
        week_day: week_day_index,
        start   : startISO,
        end     : endISO,
        topics  : recurrent.extendedProps.eventTopics,
    }
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};

export const deleteRecurrent = async (token, recurrent) => {
  
    const startISO = dateFormater(recurrent.start);

    const indice = dias.indexOf(oldRecurrent.extendedProps.day)
    const week_day_index = indice == 0 ? 7 : indice

    const url = `${apiServerUrl}/recurrent`
                + `?prof_id=${encodeURIComponent(prof_id)}`
                + `&week_day=${encodeURIComponent(week_day)}`
                + `&start=${encodeURIComponent(startISO)}`;

    const config = {
        url,
        method: "DELETE",
        headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
        },
    };

    const { data, error } = await callExternalApi({ config });

    return {
        data: data,
        error,
    };
};