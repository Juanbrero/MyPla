const LoginButton = () => {
    const handleLogin = () => {
      window.location.href = 'http://localhost:8002/api/login-google';
    };
  
    return (
      <button onClick={handleLogin}>
        Iniciar sesión con Google
      </button>
    );
  };
  
export default LoginButton;