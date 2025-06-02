import { useAuth0 } from "@auth0/auth0-react"
import { useEffect } from "react"
import { testAuthService } from "../services/test-auth.service"

export const TestAuth = ({ token }) => {
    useEffect(() => {
        if (token) {
            const fetchData = async () => {
                try {
                    const {data, error} = await testAuthService(token)
                    console.log(data)
                    if (error) {
                        console.log(error)
                    }
                } catch (err) {
                    console.log(err)
                }
            }
            fetchData()
        }
    }, [token])
    
    return (
        <h1>Test de Autorización</h1>
    )
}