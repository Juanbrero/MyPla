import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { UserTypeForm } from "../components/UserTypeForm";

export const ProfilePage = () => {
  const { user, getAccessTokenSilently, isLoading } = useAuth0();
  const [tipoUsuario, setTipoUsuario] = useState(null);

  useEffect(() => {
    if (user?.user_metadata?.tipo_usuario) {
      setTipoUsuario(user.user_metadata.tipo_usuario);
    }
  }, [user]);

  if (isLoading) return <p>Cargando perfil...</p>;

  return (
    <div>
      <h2>Perfil</h2>

      <p><strong>Nombre:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>

      {tipoUsuario ? (
        <p><strong>Tipo de usuario:</strong> {tipoUsuario}</p>
      ) : (
        <div>
          <p>No seleccionaste tu tipo de usuario. Por favor, completalo:</p>
          <UserTypeForm />
        </div>
      )}
    </div>
  );
};