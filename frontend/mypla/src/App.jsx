import { Route, Routes } from "react-router-dom"
import { AuthenticationGuard } from "./components/AuthenticationGuard"
import { ProfilePage } from "./pages/ProfilePage"
import CallbackPage from "./pages/CallbackPage"
import { ProtectedPage } from "./pages/ProtectedPage"
import OAuthCallback from "./OAuthCallback"
import { useAuth0 } from "@auth0/auth0-react"
// import ScheduleManager from './components/ScheduleManager';
import Home from "./pages/Home"
import TutorialGuide from "./components/TutorialGuide"
import { TutorialProvider } from "./components/TutorialContext"
import Calendario from "./components/shedule/Calendario"
import { TestAuth } from "./pages/TestAuth"


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
      <>
        <TutorialProvider>
          <TutorialGuide />
        </TutorialProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route 
            path="/calendar" 
            element={<AuthenticationGuard Component={Calendario} roles={["Profesional"]} />} 
          />
          <Route
            path="/profile"
            element={<AuthenticationGuard Component={ProfilePage} />}
          />
          <Route
            path="/callback"
            element={<AuthenticationGuard Component={CallbackPage} />}
          />
          <Route
            path="/protected"
            element={<AuthenticationGuard Component={ProtectedPage} />}
          />
          <Route path="/oauth-callback" element={<OAuthCallback />} />
          {/* <Route path="/test" element={<ScheduleManager />} /> */}
          <Route 
            path="/test-auth" 
            element={<AuthenticationGuard Component={TestAuth} />} 
          />
          <Route path="*" element={<h1>404 - Página no encontrada</h1>} />
        </Routes>
      </>
    )
}

export default App