import axios from 'axios';

// Creo el componente TestButton
function TestButton() {
  // defino su funcionalidad con una funcion asincronica (utilizar siempre para consultas a bd o en red)
  const TestConnBack = async () => {
    try {
      const response = await axios.get('http://localhost:8002/');
      console.log(response.data.message);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return <button onClick={TestConnBack}>Probar Conexion con sv backend</button>;
}

export default TestButton;