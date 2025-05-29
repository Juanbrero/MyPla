import { callExternalApi } from "../external-api.service";
import { dateFormater } from "../../utils/dateFormater"

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getRecurrent = async (prof_id, token) => {

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

export const putRecurrent = async (prof_id, token, newRecurrent, oldRecurrent) => {

    const oldStartISO = dateFormater(oldRecurrent.start);
    const newStartISO = newRecurrent.start ? dateFormater(newRecurrent.start) : "";
    const newEndISO = newRecurrent.end ? dateFormater(newRecurrent.end) : "";
    const week_day_index = oldRecurrent.extendedProps.day == 0 ? 7 : oldRecurrent.extendedProps.day

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

export const postRecurrent = async (prof_id, token, recurrent) => {

    const startISO = dateFormater(recurrent.start);
    const endISO = dateFormater(recurrent.end);

    const week_day_index = recurrent.extendedProps.day == 0 ? 7 : recurrent.extendedProps.day

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

export const deleteRecurrent = async (prof_id, token, recurrent) => {
  
    const startISO = dateFormater(recurrent.start);

    const week_day = recurrent.extendedProps.day == 0 ? 7 : recurrent.extendedProps.day

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