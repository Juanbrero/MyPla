import { useEffect, useState } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { Button, Box, Typography } from '@mui/material';
import ScheduleTopics from '../components/shedule/schedule-components/ScheduleTopics';
import { getTopics, postTopic } from '../services/topics/topics.service';


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
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '400px', margin: '0 auto' }}>
      {/* Sección Agregar */}
      <div>
        <h3>Agregar nuevo tópico</h3>
        <input
          type="text"
          value={newTopic}
          onChange={(e) => setNewTopic(e.target.value)}
          placeholder="Nuevo tópico"
          style={{ width: '100%', padding: '8px' }}
        />
        <button onClick={handleAdd} style={{ marginTop: '10px' }}>Agregar</button>
      </div>

      {/* Sección Mostrar */}
      <div>
        <h3>Tópicos disponibles</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {topics.map((topic) => (
            <div
              key={topic}
              style={{
                backgroundColor: '#1cb698',
                color: '#fff',
                padding: '6px 12px',
                borderRadius: '20px',
                fontSize: '0.9rem',
              }}
            >
              {topic}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
