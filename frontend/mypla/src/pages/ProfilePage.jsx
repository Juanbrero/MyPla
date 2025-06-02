import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import ProfessionalProfile from '../components/ProfessionalProfile.jsx'
import { prof_id } from "../utils/testData";
import { LinkCalendar } from "../components/LinkCalendar.jsx";
import {
  Button
} from '@mui/material';
import { useNavigate } from 'react-router-dom'

export const ProfilePage = ({token}) => {
  const { user, logout } = useAuth0();
  const [tipoUsuario, setTipoUsuario] = useState(null);

  // Obtengo la metadata de user
  const metadata = user?.[import.meta.env.VITE_NAMESPACE];

  useEffect(() => {
    // para acceder a la metadata del user (ver username, rol, etc) hay que pegarle a la management API de auth0. PENDIENTE
    if (metadata?.tipo_usuario) {
      setTipoUsuario(metadata.tipo_usuario);
      console.log(metadata)
    }
    console.log(metadata)
  }, [user]);

  // console.log("tipo usuario: " + metadata?.tipo_usuario);
  // console.log("USER", user);
  // console.log("NAMESPACE", import.meta.env.VITE_NAMESPACE);
  // console.log("METADATA", user?.[import.meta.env.VITE_NAMESPACE]);
  // getAccessTokenSilently().then(token => console.log("AccessToken", token));

  return (
    <div>
      <h2>Perfil</h2>

      <p><strong>Nombre:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <div className="prof-topics">
        <ProfessionalProfile token={token}></ProfessionalProfile>
      </div>

      {tipoUsuario ? (
        <>
          <p><strong>Tipo de usuario:</strong> {tipoUsuario}</p>
        </>
      ) : (
        <div>
          {/* <p>No seleccionaste tu tipo de usuario. Por favor, completalo:</p>
          <UserTypeForm /> */}
        </div>
      )} 
      
      <div className="link-agenda">
        <LinkCalendar></LinkCalendar>
      </div>
      <Button
          variant="contained"
          color="primary"
          onClick={() => logout({returnTo: window.location.origin})}
          sx={{ marginTop: 2 }}
        >
          Logout
        </Button>
    </div>
  );
};
