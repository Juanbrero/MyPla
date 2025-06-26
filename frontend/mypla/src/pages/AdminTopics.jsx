// import { useEffect, useState } from 'react';
// import { getTopics, postTopic } from '../services/topics/topics.service';
// import './styles/AdminTopics.css'


// export const AdminTopics = ({ token }) => {
    
//   const [topics, setTopics] = useState([]);
//   const [newTopic, setNewTopic] = useState('');

//   useEffect(() => {
//     fetchTopics();
//   }, []);

//   const fetchTopics = async () => {
//     const { data, error } = await getTopics();
//     if (!error) {
//       setTopics(data);
//     } else {
//       console.error("Error al obtener tópicos:", error);
//     }
//   };

//   const handleAdd = async () => {
//     if (newTopic.trim() === '') return;
//     await postTopic(newTopic.trim());
//     setNewTopic('');
//     fetchTopics();
//   };

//   return (
//     <div className="admin-topics-container">
//       {/* Sección Agregar */}
//       <div className='container-agregar'>
//         <h3>Agregar nuevo tópico</h3>
//         <div className="input-topic-container">
//           <input
//             className='admin-topics-input'
//             type="text"
//             value={newTopic}
//             onChange={(e) => setNewTopic(e.target.value)}
//             placeholder="Nuevo tópico"
//             />
//           </div>
//         <button onClick={handleAdd}>Agregar</button>
//       </div>

//       {/* Sección Mostrar */}
//       <div className='container-mostrar'>
//         <h3>Tópicos disponibles</h3>
//         <div className="mostrar-topics-disp-container">
//           {topics.map((topic) => (
//             <div className="each-topic-disp-container"
//               key={topic}
//             >
//               {topic}
//             </div>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// }

import { useEffect, useState } from 'react';
import { getTopics, postTopic } from '../services/topics/topics.service';
import './styles/AdminTopics.css';

export const AdminTopics = ({ token }) => {
  const [topics, setTopics] = useState([]);
  const [newTopic, setNewTopic] = useState('');
  const [category, setCategory] = useState('');
  const [categories, setCategories] = useState(['Programación', 'Matemática', 'Ciencias']); // Simulado
  const [newCategory, setNewCategory] = useState('');

  useEffect(() => {
    fetchTopics();
  }, []);

  const fetchTopics = async () => {
    const { data, error } = await getTopics();
    if (!error) setTopics(data);
    else console.error("Error al obtener tópicos:", error);
  };

  const handleAdd = async () => {
    if (!newTopic.trim() || (!category && !newCategory.trim())) return;
    const categoriaFinal = newCategory.trim() || category;
    await postTopic({ topic: newTopic.trim(), category: categoriaFinal });
    setNewTopic('');
    setCategory('');
    setNewCategory('');
    fetchTopics();
  };

  const handleSelectChange = (e) => {
    setCategory(e.target.value);
    if (e.target.value !== '') {
      setNewCategory('');
    }
  };

  const handleNewCategoryChange = (e) => {
    setNewCategory(e.target.value);
    if (e.target.value !== '') {
      setCategory('');
    }
  };

  return (
    <div className="admin-topics-container">
      {/* Formulario */}
      <div className='container-agregar'>
        <h3>Agregar nuevo tópico</h3>

        <form className='admin-topics-form' onSubmit={(e) => { e.preventDefault(); handleAdd(); }}>
        
          <fieldset className='admin-topics-fieldset'>
            <legend>Tópico</legend>
            <div>
              <input
                id='admin-topics-input-id'
                className='admin-topics-input'
                type="text"
                value={newTopic}
                onChange={(e) => setNewTopic(e.target.value)}
                placeholder="Nombre del tópico"
              />
              </div>
          </fieldset>

          <fieldset className='admin-topics-fieldset'>
            <legend>Categoría</legend>
            <div>
              <select
                className='admin-topics-select'
                value={category}
                onChange={handleSelectChange}
                disabled={newCategory !== ''}
                >
                <option value="">Seleccionar categoría existente</option>
                {categories.map((cat, i) => (
                  <option key={i} value={cat}>{cat}</option>
                ))}
              </select>
            </div>
            <div>
              <input
                className='admin-topics-input'
                type="text"
                value={newCategory}
                onChange={handleNewCategoryChange}
                placeholder="O crear nueva categoría"
                disabled={category !== ''}
              />
            </div>
          </fieldset>

          <button
            type="submit"
            disabled={!newTopic.trim() || (!category && !newCategory.trim())}
          >
            Agregar
          </button>

        </form>

      </div>

      {/* Mostrar tópicos */}
      <div className='container-mostrar'>
        <h3>Tópicos disponibles</h3>
        <div className="mostrar-topics-disp-container">
          {topics.map((topic, i) => (
            <div className="each-topic-disp-container" key={i}>
              {topic}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
