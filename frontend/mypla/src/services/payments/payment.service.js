import { callExternalApi } from "../external-api.service";
const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const getPayPending = async (token) => {

    const config = {
        url: `${apiServerUrl}/pay/pending`,
        method: "GET",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`,
        }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data;
};

export const putPayPending = async (token, body) => {

    const config = {
        url: `${apiServerUrl}/pay/pending`,
        method: "PUT",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        data: {
            day_hour: body.day_hour,
            prof_id: body.user_professional.professional_id,
            student_id: body.user_student.student_id,
        }
    };

    const { data, error } = await callExternalApi({ config });

    if (error) {
      console.error("Error al obtener datos:", error);
      throw error;
    }

    return data;
};

