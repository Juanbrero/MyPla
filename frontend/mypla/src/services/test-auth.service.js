import { callExternalApi } from "./external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const testAuthService = async (accessToken) => {
    console.log(accessToken)
  const config = {
    url: `${apiServerUrl}/test-professional`,
    method: "GET",
    //credentials: "include",
    headers: {
      "content-type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
  };

  console.log(config)

  const { data, error } = await callExternalApi({ config });

  return {
    data: data || null,
    error,
  };
};