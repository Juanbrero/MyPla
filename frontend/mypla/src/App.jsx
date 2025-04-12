import { Route, Routes } from "react-router-dom"
import { AuthenticationGuard } from "./components/AuthenticationGuard"
import { ProfilePage } from "./pages/ProfilePage"
import CallbackPage from "./pages/CallbackPage"
import { ProtectedPage } from "./pages/ProtectedPage"
import OAuthCallback from "./OAuthCallback"
import { useAuth0 } from "@auth0/auth0-react"
import Home from "./pages/Home"


const App = () => {
    const { isLoading } = useAuth0();

    if (isLoading) {
      return (
        <div className="page-layout">
          ... carregando
        </div>
      );
    }

    return (
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/profile"
            element={<AuthenticationGuard component={ProfilePage} />}
          />
          <Route
            path="/callback"
            element={<AuthenticationGuard component={CallbackPage} />}
          />
          <Route
            path="/protected"
            element={<AuthenticationGuard component={ProtectedPage} />}
          />
          <Route path="/oauth-callback" element={<OAuthCallback />} />
          <Route path="*" element={<h1>404 - Página no encontrada</h1>} />
        </Routes>
    )
}

export default App