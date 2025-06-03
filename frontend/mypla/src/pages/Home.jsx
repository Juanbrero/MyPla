import { useState } from 'react'
import '../App.css'
import { LoginButton } from '../components/auth0Buttons/LoginButton'
import { SignupButton } from '../components/auth0Buttons/SignUpButton'

function Home() {
  const [count, setCount] = useState(0)

  return (
    <>
      
      <h1>Bienvenido a <span style={{color: '#1cb6ae'}}>MiPla!</span></h1>
      
      
      {/* <div className='paypalButton'>
          <PayPalButton></PayPalButton>
      </div>
      <div className="mpButton">
          <MPButton></MPButton> */}
      {/* </div> */}
      <div className='loginButtons'>
        <LoginButton />
        <SignupButton />
      </div>

    </>
  )
}

export default Home
