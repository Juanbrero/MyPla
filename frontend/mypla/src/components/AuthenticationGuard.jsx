import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react";
import React, { useState, useEffect } from "react";

export const AuthenticationGuard = ({ Component }) => {
  const [accessToken, setAccessToken] = useState()
  const { getAccessTokenSilently, isAuthenticated, isLoading } = useAuth0()

  useEffect(() => {
    const fetchToken = async () => {
      if (isAuthenticated) {
        const token = await getAccessTokenSilently({
          audience: import.meta.env.VITE_AUTH0_AUDIENCE
        })

        setAccessToken(token)
      }
    }
    fetchToken()
  }, [])

  const ComponentRender = withAuthenticationRequired(Component, {
    onRedirecting: () => (
      <div className="page-layout">
        ...
      </div>
    ),
  });

  if (isLoading) {
    return <div>Verificando autenticación...</div>;
  }

  return <ComponentRender token={accessToken} />;
};
