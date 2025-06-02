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

export const putException = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/exception?prof_id=${encodeURIComponent(prof_id)}`,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    data: {
      day: body.day,
      start: body.start,
      Nday: body.Nday,
      Nstart: body.Nstart,
      Nend: body.Nend
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};

export const postException = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/exception?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: {
      day: body.day,
      start: body.start,
      end: body.end
    }
  };

  const { data, error } = await callExternalApi({ config });

  return {
      data: data,
      error,
  };
};

export const deleteException = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/exception?prof_id=${encodeURIComponent(prof_id)}`,
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
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