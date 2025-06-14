import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react";
import React, { useState, useEffect } from "react";

export const AuthenticationGuard = ({ Component, roles = [], renderAlways }) => {
  const [accessToken, setAccessToken] = useState()
  const { user, getAccessTokenSilently, isAuthenticated, isLoading } = useAuth0()

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

  // Verifica si el usuario tiene al menos uno de los roles requeridos
  const userRoles = user?.[import.meta.env.VITE_NAMESPACE + '/roles'] || []; // Obtiene los roles del usuario
  const hasRequiredRole = () => {
    if (!roles.length) return true; // Si no hay roles requeridos, permite el acceso
    return roles.some(role => userRoles.includes(role));
  };

  const ComponentRender = !renderAlways ? withAuthenticationRequired(Component, {
    onRedirecting: () => (
      <div className="page-layout">
        ...
      </div>
    ),
  }) : Component;

  if (renderAlways) {
    return <ComponentRender token={accessToken} roles={userRoles} />
  }

  if (isLoading || accessToken === undefined) {
    return;
  }
  
  if (!hasRequiredRole()) {
    return <div>No tienes permisos para acceder a esta página.</div>;
  }

  return <ComponentRender token={accessToken} roles={userRoles} />;
};
