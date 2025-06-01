import { callExternalApi } from "../services/external-api.service";


const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;


export const getAvailableProfessional = async (prof_id) => {
  const config = {
    url: `${apiServerUrl}/available/professionals?prof_id=${encodeURIComponent(prof_id)}`,
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  };

  const { data, error } = await callExternalApi({ config });

  if (error) {
    console.error("Error al obtener datos:", error);
    throw error;
  }

  // Procesar la respuesta para agregar el campo 'type' a cada objeto, manteniendo la estructura original
  const result = {};

  for (const [key, items] of Object.entries(data)) {
    if (Array.isArray(items)) {
      result[key] = items.map((item) => ({
        ...item,
        type: key, // Agregar el campo 'type' con el nombre de la clave
      }));
    } else {
      result[key] = items;
    }
  }

  return result;
};

export const postSpecific = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
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

export const putSpecific = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
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

export const deleteSpecific = async (prof_id, body) => {
  const config = {
    url: `${apiServerUrl}/specific?prof_id=${encodeURIComponent(prof_id)}`,
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

export const getProfessionalTopics = async (prof_id) => {

    const config = {
    url: `${apiServerUrl}/professionals-topic?prof_id=${encodeURIComponent(prof_id)}`,
    method: "GET",
    headers: {
        "content-type": "application/json",
    }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    const topics = Array.isArray(data)
        ? data.map(item => item.topic_name)
        : [];


    return topics;
};