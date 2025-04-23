// src/components/UserTypeForm.js
import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { sendUserType } from "../services/user.service";
import { UserTypeSelector } from "./UserTypeSelector";

export const UserTypeForm = () => {
  const { user, getAccessTokenSilently } = useAuth0();
  const [status, setStatus] = useState("");

  const handleUserTypeSelected = async (selectedType) => {
    try {
      const token = await getAccessTokenSilently();
      const response = await sendUserType({
                                          userId: user.sub, 
                                          tipoUsuario: selectedType, 
                                          token: token,
                                        });

      if (response?.data?.message === "User type updated") {
        setStatus("Guardado correctamente ✅");
        // Refrescamos el perfil completo
        window.location.reload();
      } else {
        setStatus("Error al guardar ❌");
      }
    } catch (error) {
      console.error("Error al guardar tipo de usuario:", error);
      setStatus("Error al guardar ❌");
    }
  };

  return (
    <div>
      <UserTypeSelector onUserTypeSelected={handleUserTypeSelected} />
      <p>{status}</p>
    </div>
  );
};
