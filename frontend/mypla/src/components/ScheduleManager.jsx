import React, { useState } from 'react';
import { Button } from '@mui/material';
import ScheduleCreate from './ScheduleCreate';
import ScheduleEdit from './ScheduleEdit';

export default function ScheduleManager() {
  const initialTask = {
    topics: ['Estrategia', 'Marketing'],
    day: 'Martes',
    start: '14:00',
    end: '15:00',
    recurrent: true,
    date: "2025-04-18",
  };

  const [selectedTask, setSelectedTask] = useState(initialTask);
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [infoModalOpen, setInfoModalOpen] = useState(false);

  const handleOpenCreateModal = () => {
    setCreateModalOpen(true);
  };

  const handleCloseCreateModal = () => {
    setCreateModalOpen(false);
  };

  const handleOpenInfoModal = () => {
    setInfoModalOpen(true);
  };

  const handleCloseInfoModal = () => {
    setInfoModalOpen(false);
  };

  const handleCancelTask = (taskName) => {
    console.log('Cancelando toda la tarea:', taskName);
    // lógica para cancelar toda la tarea
  };

  const handleSaveTask = (updatedTask) => {
    console.log('Guardando la tarea:', updatedTask);
    setSelectedTask({
      ...updatedTask,
      start: updatedTask.startTime,
      end: updatedTask.endTime,
      recurrent: updatedTask.isRecurring,
    });
    setCreateModalOpen(false);
    setInfoModalOpen(false);
  };

  return (
    <div>
      <h2>Agregar Horario</h2>
      <Button variant="contained" onClick={handleOpenCreateModal}>
        Abrir para crear
      </Button>

      <ScheduleCreate
        open={createModalOpen}
        onClose={handleCloseCreateModal}
        taskData={selectedTask}
        onCancelTask={handleCancelTask}
        onSaveTask={handleSaveTask}
      />

      <h2>Ver, editar, borrar</h2>
      <Button variant="contained" onClick={handleOpenInfoModal}>
        Abrir para ver información
      </Button>

      <ScheduleEdit
        open={infoModalOpen}
        onClose={handleCloseInfoModal}
        taskData={selectedTask}
        onCancelTask={handleCancelTask}
        onSaveTask={handleSaveTask}
      />
    </div>
  );
}
