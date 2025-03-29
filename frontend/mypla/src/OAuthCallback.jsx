import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const OAuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Este efecto se corre al cargar /callback
    const handleAuth = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code');

      if (code) {
        // El backend hace el intercambio por token
        const res = await fetch(`http://localhost:8002/auth${location.search}`, {
          credentials: 'include',
        });
        const data = await res.json();
        console.log('Usuario:', data.user);
        navigate('/');
      }
    };

    handleAuth();
  }, [location, navigate]);

  return <div>Autenticando...</div>;
};

export default OAuthCallback;