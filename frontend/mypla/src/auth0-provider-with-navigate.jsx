import { Auth0Provider } from "@auth0/auth0-react";
import React from "react";
import { useNavigate } from "react-router-dom";

export const Auth0ProviderWithNavigate = ({ children }) => {
  const navigate = useNavigate();
  console.log("ESTAS ACA")

  const domain = /*process.env.VITE_AUTH0_DOMAIN ??*/ 'dev-znigqrdhldkrdh61.us.auth0.com';
  const clientId = /*process.env.VITE_AUTH0_CLIENT_ID ??*/ '69BHYcnc7PNDu17qMhf2jOxa2zflKy99';
  const redirectUri = /*process.env.VITE_AUTH0_CALLBACK_URL ??*/ 'http://localhost:3000/callback';
  const audience = /*process.env.VITE_AUTH0_AUDIENCE ??*/ 'https://hello-world.example.com';

  const onRedirectCallback = (appState) => {
    navigate(appState?.returnTo || window.location.pathname);
  };

  if (!(domain && clientId && redirectUri && audience)) {
    return null;
  }

  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        audience: audience,
        redirect_uri: redirectUri,
      }}
      onRedirectCallback={onRedirectCallback}
    >
      {children}
    </Auth0Provider>
  );
};
