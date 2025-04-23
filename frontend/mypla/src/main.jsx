import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from "react-router-dom";
import './index.css'
import App from './App.jsx'
import OAuthCallback from './OAuthCallback.jsx';
import { ProtectedPage } from './pages/ProtectedPage.jsx';
import { AuthenticationGuard } from './components/AuthenticationGuard.jsx';
import { Auth0ProviderWithNavigate } from './auth0-provider-with-navigate.jsx';
import { ProfilePage } from './pages/ProfilePage.jsx';
import CallbackPage from './pages/CallbackPage.jsx';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <StrictMode>
    <BrowserRouter>
      <Auth0ProviderWithNavigate>
        <App />
      </Auth0ProviderWithNavigate>
    </BrowserRouter>
  </StrictMode>
)
