import { Modal } from '@mui/material';
import { useEffect, useState } from 'react';
import React from 'react';
import ReservationStep from './reservation-steps/ReservationStep';
import PaymentStep from './reservation-steps/PaymentStep';
import ConfirmStep from './reservation-steps/ConfirmStep';
import SelectStep from './reservation-steps/SelectStep';


const steps = ["SELECT", "RESERVATION", "PAYMENT", "CONFIRMATION"];

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

export default function ReservationModal({
  open,
  onClose,
  taskData,
}) {

    const [step, setStep] = useState(steps[0]);
    const [localTaskData, setLocalTaskData] = React.useState(taskData);

    useEffect (() => {
        setLocalTaskData(taskData);
        if (taskData) taskData.selectedTopic = taskData.topics[0];
    }, [taskData])

    const goToStep = (nextStep) => {
        setStep(nextStep);
    }

    const handleClose = () => {
        onClose?.();
        setStep(steps[0]);
    };

    const handleTaskDataChange = (partialUpdate) => {
        setLocalTaskData((prev) => ({
        ...prev,
        ...partialUpdate,
        }));
    };

    const renderStep = (step) => {
        switch (step) {
            case "SELECT":
                return <SelectStep
                            taskData={taskData} 
                            onClose={handleClose}
                            onChange={handleTaskDataChange}
                            onNext={() => goToStep(steps[1])}
                            style={style} />
            case "RESERVATION":
                return <ReservationStep 
                            taskData={localTaskData} 
                            onClose={handleClose}
                            onNext={() => goToStep(steps[2])}
                            style={style} />;
            case "PAYMENT":
                return <PaymentStep 
                            reservationInfo={localTaskData}
                            onClose={handleClose}
                            onNext={() => goToStep(steps[3])}
                            style={style} />;
            case "CONFIRMATION": 
                return <ConfirmStep 
                            taskData={localTaskData} 
                            onClose={handleClose}
                            style={style} />;
        }
    }

    return (
        <Modal open={open} onClose={onClose}>
            
            {renderStep(step)}
            
        </Modal>
    )

}