import { useAuth0 } from "@auth0/auth0-react";

export const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  const handleLogin = async () => {
    await loginWithRedirect({
      appState: {
        returnTo: "/profile",
      },
      authorizationParams: {
        prompt: "login",
      },
    });
  };

  return (
    <li className="button__login" onClick={handleLogin}>
      Login
    </li>
    // <button className="button__login" onClick={handleLogin}>
    //   Log In
    // </button>
  );
};