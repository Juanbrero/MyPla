import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import ProfessionalProfile from '../components/ProfessionalProfile.jsx'
import StudentProfile from '../components/StudentProfile.jsx'
import { prof_id } from "../utils/testData";
import { LinkCalendar } from "../components/LinkCalendar.jsx";
import {
  Button
} from '@mui/material';

export const ProfilePage = ({token, roles}) => {
  const { user, logout } = useAuth0();
  const [tipoUsuario, setTipoUsuario] = useState(null);

  const metadata = user?.[import.meta.env.VITE_NAMESPACE];

  useEffect(() => {
    if (metadata?.tipo_usuario) {
      setTipoUsuario(metadata.tipo_usuario);
    }
  }, [user]);

  return (
    <div>
      {roles.includes("Profesional") &&
        <div className="prof-topics">
          <ProfessionalProfile token={token} user={user}></ProfessionalProfile>
        </div>
      }
      {roles.includes("Alumno") &&
        <StudentProfile token={token} user={user}></StudentProfile>
      }
      
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
