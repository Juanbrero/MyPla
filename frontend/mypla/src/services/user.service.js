import { callExternalApi } from "./external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;// ?? "http://localhost:8002";

export const sendUserType = async ({ userId, tipoUsuario, token }) => {
  const config = {
    url: `${apiServerUrl}/api/user/type`,
    method: "POST",
    headers: {
      "content-type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    data: {
      user_id: userId,
      tipo_usuario: tipoUsuario,
    },
  };

  const { data, error } = await callExternalApi({ config });

  return {
    data: data || null,
    error,
  };
};
