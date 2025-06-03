import { Box, Button, Typography, Modal } from '@mui/material';
import ScheduleTopics from '../shedule/schedule-components/ScheduleTopics';
import ScheduleDate from '../shedule/schedule-components/ScheduleDate';
import ScheduleTime from '../shedule/schedule-components/ScheduleTime';
import { useEffect, useState } from 'react';
import ReservationStep from './reservation-steps/ReservationStep';
import PaymentStep from './reservation-steps/PaymentStep';
import ConfirmStep from './reservation-steps/ConfirmStep';


const steps = ["RESERVATION", "PAYMENT", "CONFIRMATION"];

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

    const goToStep = (nextStep) => {
        setStep(nextStep);
    }

    const handleClose = () => {
        onClose?.();
        setStep(steps[0]);
    };

    const renderStep = (step) => {
        switch (step) {
            case "RESERVATION":
                return <ReservationStep 
                            taskData={taskData} 
                            onClose={handleClose}
                            onNext={() => goToStep(steps[1])}
                            style={style} />;
            case "PAYMENT":
                return <PaymentStep 
                            onClose={handleClose}
                            onNext={() => goToStep(steps[2])}
                            style={style} />;
            case "CONFIRMATION": 
                return <ConfirmStep 
                            taskData={taskData} 
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