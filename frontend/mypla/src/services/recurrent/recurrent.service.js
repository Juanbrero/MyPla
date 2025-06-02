import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getRecurrent = async (prof_id) => {

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

export const putRecurrent = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent?prof_id=${encodeURIComponent(prof_id)}`,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    data: {
      week_day: body.week_day,
      start: body.start,
      Nweek_day: body.Nweek_day,
      Nstart: body.Nstart,
      Nend: body.Nend,
      topics: body.topics
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
}

export const postRecurrent = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: {
      week_day: body.week_day,
      start: body.start,
      end: body.end,
      topics: body.topics
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
}

export const deleteRecurrent = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent?prof_id=${encodeURIComponent(prof_id)}&week_day=${encodeURIComponent(body.week_day)}&start=${encodeURIComponent(body.start)}`,
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};