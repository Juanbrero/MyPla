import { Route, Routes } from "react-router-dom"
import { AuthenticationGuard } from "./components/AuthenticationGuard"
import { ProfilePage } from "./pages/ProfilePage"
import CallbackPage from "./pages/CallbackPage"
import { ProtectedPage } from "./pages/ProtectedPage"
import OAuthCallback from "./OAuthCallback"
import { useAuth0 } from "@auth0/auth0-react"
import Home from "./pages/Home"
import TutorialGuide from "./components/TutorialGuide"
import { TutorialProvider } from "./components/TutorialContext"
import CalendarioWrapper from "./components/wrappers/CalendarioWrapper.jsx"
import { TestAuth } from "./pages/TestAuth"
import { HeaderComponent } from './components/header/HeaderComponent.jsx'
import { ProfessionalsList } from './pages/ProfessionalsList.jsx'
import StudentCalendar from "./components/studentCalendar/StudentCalendar.jsx"


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
      <AuthenticationGuard Component={HeaderComponent} roles={[]} />
        
        <TutorialProvider>
          <TutorialGuide />
        </TutorialProvider>
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
             path="/calendar/:prof_id" 
             element={<AuthenticationGuard Component={StudentCalendar} roles={["Alumno"]} />}
          />
          <Route 
            path="/calendar" 
            element={<AuthenticationGuard Component={CalendarioWrapper} roles={["Profesional", "Alumno"]} />} 
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
          <Route 
            path="/professionalsList" 
            element={<AuthenticationGuard Component={ProfessionalsList} />} 
          />
          <Route path="*" element={<h1>404 - Página no encontrada</h1>} />
        </Routes>
      </>
    )
}

export default App