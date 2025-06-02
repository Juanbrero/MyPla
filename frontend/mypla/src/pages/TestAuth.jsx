import { useAuth0 } from "@auth0/auth0-react"
import { useEffect } from "react"
import { testAuthService } from "../services/test-auth.service"

export const TestAuth = () => {
    const { isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0()
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                if (isLoading) return
                console.log(isAuthenticated, "AUTHENTICATED")
                if (isAuthenticated) {
                    const token = await getAccessTokenSilently({
                        audience: import.meta.env.VITE_AUTH0_AUDIENCE
                    })
                    const {data, error} = await testAuthService(token)
                    console.log(data)
                    if (error) {
                        console.log(error)
                    }
                }
            } catch (err) {
                console.log(err)
            }
        }
        fetchData()
    }, [])
    
    return (
        <h1>Test de Autorización</h1>
    )
}