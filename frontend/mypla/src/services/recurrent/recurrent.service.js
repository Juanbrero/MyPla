import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getRecurrent = async () => {

    const config = {
    url: `${apiServerUrl}/recurrent`,
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

export const putRecurrent = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent`,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
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

export const postRecurrent = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
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

export const deleteRecurrent = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/recurrent?week_day=${encodeURIComponent(body.week_day)}&start=${encodeURIComponent(body.start)}`,
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};