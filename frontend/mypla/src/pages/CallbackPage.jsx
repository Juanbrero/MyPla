import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";


const CallbackHandler = () => {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [tipoUsuario, setTipoUsuario] = useState(null);

  const backendUrl = import.meta.env.VITE_API_SERVER_URL;

  useEffect(() => {
    if (isAuthenticated && tipoUsuario) {
      const sendUserType = async () => {
        const token = await getAccessTokenSilently();
        await axios.post(`${backendUrl}/api/user/type`, {
          user_id: user.sub,
          tipo_usuario: tipoUsuario,
        });
      };

      sendUserType();
    }
  }, [isAuthenticated, tipoUsuario, user]);

  return (
    <div>
      {isAuthenticated ? (
        <>
          <h3>Bienvenido, {user.name}</h3>
          
        </>
      ) : (
        <p>Iniciando sesión...</p>
      )}
    </div>
  );
};

export default CallbackHandler;