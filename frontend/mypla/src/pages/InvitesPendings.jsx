import { useAuth0 } from '@auth0/auth0-react';
import { useEffect, useState } from 'react';
import React from 'react';
import './styles/InvitesPendings.css';
import InvitesModal from '../components/invites/InvitesModal'
import { getHour } from '../utils/dateFormater';
import { getInvites } from '../services/invites/invites.service';


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

export default function InvitesPending({
  token,
}) {

  const { isAuthenticated } = useAuth0();
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);
  const [invites, setInvites] = useState([]);

  useEffect(() => {
    const cargarInvitacionesPendientes = async () => {
      try {
        const response = await getInvites(token);
        const invitesPendings = response?.data || [];
        setInvites(invitesPendings);

        console.log(response);

      } catch (error) {
        console.error("Error al obtener invitaciones pendientes:", error);
      }
    };

    if (isAuthenticated) {
      cargarInvitacionesPendientes();
    }
  }, [isAuthenticated, token]);

  const handleRowClick = (invite) => {
    const prof_id = invite.invite.prof_id;
    const day_hour = invite.invite.day_hour;
    const professional_username = invite.professional_username;
    const title = invite.event.title;
    const date = new Date(invite.event.day_hour).toLocaleDateString();
    const hour = getHour(invite.event.day_hour);
    const duration = (invite.event.duration / 60);

    setSelectedRow({ prof_id, professional_username, title, date, hour, duration, day_hour });
    setModalOpen(true);
  };


  return (
    <div id="gral-invites-table-container">
      <div id="table-invites-title-container">
        <h2>Invitaciones pendientes</h2>
      </div>

      <div id="table-invites-container">
        <table id="invites-table">
          <thead>
            <tr>
              <th className="invites-inviteDate">Fecha De Invitacion</th>
              <th className="invites-prof">Anfitrion</th>
              <th className="invites-title">Titulo Del Evento</th>
              <th className="invites-date">Fecha</th>
              <th className="invites-hour">Hora de inicio</th>
              <th className="invites-duration">Duracion</th>
            </tr>
          </thead>
          <tbody>
            {invites.map((invite, index) => (
              <tr key={index} onClick={() => handleRowClick(invite)}>
                <td>{new Date(invite.invite.create).toLocaleDateString()}</td>
                <td>{invite.professional_username}</td>
                <td>{invite.event.title}</td>
                <td>{new Date(invite.invite.day_hour).toLocaleDateString()}</td>
                <td>{getHour(invite.event.day_hour)}</td>
                <td>{(invite.event.duration) / 60} hs</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedRow && (
        <InvitesModal
          open={modalOpen}
          onClose={() => setModalOpen(false)}
          token={token}
          event={selectedRow}
        />
      )}
    </div>
  );

}