import { useAuth0 } from '@auth0/auth0-react';
import { useEffect, useState } from 'react';
import React from 'react';
import { getCalificate } from '../services/calification/calification.service';
import CalificationModal from '../components/califications/CalificationModal';
import './styles/CalificationsPending.css';



const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 500,
  bgcolor: 'background.paper',
  borderRadius: '12px',
  boxShadow: 24,
  p: 4,
  color: 'text.primary',
  overflowY: 'auto',
  maxHeight: '90vh',
};

export default function CalificationsPending({
  token,
}) {

  const { isAuthenticated } = useAuth0();
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);
  const [califications, setCalifications] = useState([]);

  useEffect(() => {
    const cargarCalificacionesPendientes = async () => {
      try {
        const response = await getCalificate(token);
        const califPendings = response?.data?.calificate || [];
        setCalifications(califPendings);

        console.log(response);

      } catch (error) {
        console.error("Error al obtener calificaciones pendientes:", error);
      }
    };

    if (isAuthenticated) {
      cargarCalificacionesPendientes();
    }
  }, [isAuthenticated, token, modalOpen]);

  const handleRowClick = (calif) => {
    const date = new Date(calif.day_hour).toLocaleDateString();
    const prof_id = calif.prof_id;
    const prof_username = calif.prof_username;
    const day_hour = calif.day_hour;

    setSelectedRow({ prof_id, prof_username, day_hour, date });
    setModalOpen(true);
  };

  return (
    <div id="gral-califications-table-container">
      <div id="table-califications-title-container">
        <h2>Calificaciones pendientes</h2>
      </div>

      <div id="table-califications-container">
        <table id="califications-table">
          <thead>
            <tr>
              <th className="calif-prof">Profesional</th>
              <th className="calif-topic">Topico</th>
              <th className="calif-date">Fecha</th>
            </tr>
          </thead>
          <tbody>
            {califications.map((calif, index) => (
              <tr key={index} onClick={() => handleRowClick(calif)}>
                <td>{calif.prof_username}</td>
                <td>{calif.topic}</td>
                <td>{new Date(calif.day_hour).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedRow && (
        <CalificationModal
          open={modalOpen}
          onClose={() => setModalOpen(false)}
          token={token}
          class_id={selectedRow}
        />
      )}
    </div>
  );

}