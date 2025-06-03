import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getSpecific = async (token) => {

    const config = {
    url: `${apiServerUrl}/specific`,
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

export const putSpecific = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/specific`,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    data: {
      day: body.day,
      start: body.start,
      Nday: body.Nday,
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
};

export const postSpecific = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/specific`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    data: {
      day: body.day,
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
};

export const deleteSpecific = async (token, body) => {
  const config = {
    url: `${apiServerUrl}/specific`,
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    data: {
      day: body.day,
      start: body.start
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};