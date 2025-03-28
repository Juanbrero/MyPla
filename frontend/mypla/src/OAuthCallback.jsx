import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const OAuthCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    if (code) {
      // Mandamos el código al backend
      fetch('http://localhost:8002/api/auth-callback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
        credentials: 'include', // si manejás cookies / sesiones
      })
        .then(res => res.json())
        .then(data => {
          console.log('Usuario autenticado:', data);
          // Guardar token en localStorage o estado global si hace falta
          navigate('/dashboard'); // redirigir a donde quieras
        })
        .catch(err => {
          console.error('Error al autenticar:', err);
        });
    }
  }, [navigate]);

  return <p>Autenticando...</p>;
};

export default OAuthCallback;