import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import ProfessionalProfile from '../components/ProfessionalProfile.jsx'
import StudentProfile from '../components/StudentProfile.jsx'
import AdminProfile from '../components/AdminProfile.jsx'


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
      {roles.includes("Administrador") &&
        <AdminProfile token={token} user={user}></AdminProfile>
      }
      
    </div>
  );
};
