import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import MPButton from './MPButton.jsx'
import PayPalButton from './PayPalButton.jsx'
import ButtonLoginGoogle from './ButtonLoginGoogle.jsx'
import { LoginButton } from './components/buttons/LoginButton.jsx'
import { SignupButton } from './components/buttons/SignUpButton.jsx'

function Home() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      
      </div>
      
      <PayPalButton></PayPalButton>
      <MPButton></MPButton>
      <ButtonLoginGoogle />
      <LoginButton />
      <SignupButton />

    </>
  )
}

export default Home
