import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

function Google() {
  return (
    <GoogleOAuthProvider clientId="943184283815-8msdh7njimvd3a77gtnoor5prj9gdnnl.apps.googleusercontent.com">
      <GoogleLogin
        onSuccess={async (credentialResponse) => {
          const res = await fetch('http://localhost:8002/api/google-auth', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: credentialResponse.credential }),
          });
          console.log(res)
        }}
        onError={() => {
          console.log('Login Failed');
        }}
      />
    </GoogleOAuthProvider>
  );
}

export default Google