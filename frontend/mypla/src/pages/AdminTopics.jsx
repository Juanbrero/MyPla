import { useEffect, useState } from 'react';
import { getTopics, postTopic } from '../services/topics/topics.service';
import './styles/AdminTopics.css'


export const AdminTopics = ({ token }) => {
    
  const [topics, setTopics] = useState([]);
  const [newTopic, setNewTopic] = useState('');

  useEffect(() => {
    fetchTopics();
  }, []);

  const fetchTopics = async () => {
    const { data, error } = await getTopics();
    if (!error) {
      setTopics(data);
    } else {
      console.error("Error al obtener tópicos:", error);
    }
  };

  const handleAdd = async () => {
    if (newTopic.trim() === '') return;
    await postTopic(newTopic.trim());
    setNewTopic('');
    fetchTopics();
  };

  return (
    <div className="admin-topics-container">
      {/* Sección Agregar */}
      <div className='container-agregar'>
        <h3>Agregar nuevo tópico</h3>
        <div className="input-topic-container">
          <input
            className='admin-topics-input'
            type="text"
            value={newTopic}
            onChange={(e) => setNewTopic(e.target.value)}
            placeholder="Nuevo tópico"
            />
          </div>
        <button onClick={handleAdd}>Agregar</button>
      </div>

      {/* Sección Mostrar */}
      <div className='container-mostrar'>
        <h3>Tópicos disponibles</h3>
        <div className="mostrar-topics-disp-container">
          {topics.map((topic) => (
            <div className="each-topic-disp-container"
              key={topic}
            >
              {topic}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
