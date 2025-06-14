import { useAuth0 } from "@auth0/auth0-react";
  
export const LogoutButton = () => {

    const { user, logout } = useAuth0();

    return <li className="logout-link" style={{cursor: 'pointer'}} onClick={() => logout({returnTo: '/'})}>Salir</li>

}
