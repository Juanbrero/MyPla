import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

export const ProfilePage = () => {
  const { user } = useAuth0();

  if (!user) {
    return null;
  }

  return (
    <div>
        <h1>Este es el perfil del usuario</h1>
        <p>{user.name}</p>
        <p>{user.email}</p>
    </div>
  )
}