import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
import { UserTypeSelector } from "../components/UserTypeSelector";

const CallbackHandler = () => {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [tipoUsuario, setTipoUsuario] = useState(null);

  useEffect(() => {
    if (isAuthenticated && tipoUsuario) {
      const sendUserType = async () => {
        const token = await getAccessTokenSilently();
        await axios.post("http://localhost:8002/api/user/type", {
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
          <UserTypeSelector onUserTypeSelected={setTipoUsuario} />
        </>
      ) : (
        <p>Iniciando sesión...</p>
      )}
    </div>
  );
};

export default CallbackHandler;

// import { useAuth0 } from "@auth0/auth0-react";

// const CallbackPage = () => {
//     const { error } = useAuth0();

//     if (error) {
//       return (
//           <div className="content-layout">
//             <h1 id="page-title" className="content__title">
//               Error
//             </h1>
//             <div className="content__body">
//               <p id="page-description">
//                 <span>{error.message}</span>
//               </p>
//             </div>
//           </div>
//       );
//     }
  
//     return (
//       <div className="page-layout">
//         No hubo error
//       </div>
//     );
// }

// export default CallbackPage