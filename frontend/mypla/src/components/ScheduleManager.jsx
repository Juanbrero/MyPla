import React, { useState } from 'react';
import { Button } from '@mui/material';
import ScheduleInformation from './ScheduleInformation'; // Asegurate de que la ruta esté bien

export default function ScheduleManager() {
  const [modalOpen, setModalOpen] = useState(false);

  // Simulación de una tarea seleccionada
  const [selectedTask, setSelectedTask] = useState({
    topics: ['Estrategia', 'Marketing'],
    day: 'Martes',
    start: '14:00',
    end: '15:00',
    recurrent: true,
    date: "2025-04-18",
  });

  const handleOpenModal = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  // const handleCancelSlot = ({ day, startTime, endTime }) => {
  //   console.log('Cancelando franja:', day, startTime, endTime);
  //   // acá podrías actualizar tu backend, o el estado de tareas, etc.
  // };

  const handleCancelTask = (taskName) => {
    console.log('Cancelando toda la tarea:', taskName);
    // lógica para eliminar o desactivar la tarea completa
  };

  const handleSaveTask = (taskName) => {
    console.log('Guardando la tarea:', taskName);
    // lógica para guardar la tarea
  };

  return (
    <div>
      <h2>Gestión de Tareas</h2>
      <Button variant="contained" onClick={handleOpenModal}>
        Editar tarea
      </Button>

      <ScheduleInformation
        open={modalOpen}
        onClose={handleCloseModal}
        taskData={selectedTask}
        // onCancelSlot={handleCancelSlot}
        onCancelTask={handleCancelTask}
        onSaveTask={handleSaveTask}
      />
    </div>
  );
}
