import { Modal } from '@mui/material';
import { useEffect, useState } from 'react';
import React from 'react';
import ReservationStep from './reservation-steps/ReservationStep';
import PaymentStep from './reservation-steps/PaymentStep';
import ConfirmStep from './reservation-steps/ConfirmStep';
import SelectStep from './reservation-steps/SelectStep';
import { initialClass } from '../../services/reservation/initial-class.service';
import { postReservationEvent } from '../../services/reservation/reservation-event.service';


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
  event,
  token,
  prof_id
}) {
    const [step, setStep] = useState((taskData && !event) ? steps[0] : steps[1]);
    // const [step, setStep] = useState(steps[0]);
    // const [localTaskData, setLocalTaskData] = React.useState(taskData);
    const [localTaskData, setLocalTaskData] = React.useState(taskData? taskData : null);

    console.log("step: ", step);
    useEffect (() => {
        // setLocalTaskData(taskData);
        // if (taskData) taskData.selectedTopic = taskData.topics[0];
        
        if (event && !taskData) {
            setStep(steps[1]); // "RESERVATION"
        } else if (taskData && !event) {
            setStep(steps[0]); // "SELECT"
        }

        setLocalTaskData(taskData? taskData : null);
        if (taskData) taskData.selectedTopic = taskData.topics[0];
        
    }, [taskData, event]);

    const goToStep = (nextStep) => {
        setStep(nextStep);
    }

    const handleClose = () => {
        onClose?.();
    };

    const handleTaskDataChange = (partialUpdate) => {
        setLocalTaskData((prev) => ({
        ...prev,
        ...partialUpdate,
        }));
    };

    const initialReservation = async (go) => {

        let initial = null;
        
        if (taskData && !event) {
            initial = await initialClass(token, localTaskData, prof_id);
        }
        else if (event && !taskData) {
            initial = await postReservationEvent(token, event, prof_id);
        }
        
        // const initial = await initialClass(token, localTaskData, prof_id)
        if (initial) {
            go()
        }
    } 

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
                            event = {event}
                            onClose={handleClose}
                            onNext={async() => await initialReservation(() => goToStep(steps[2]))}
                            style={style} />;
            case "PAYMENT":
                return <PaymentStep 
                            reservationInfo={localTaskData}
                            event = {event}
                            onClose={handleClose}
                            onNext={() => goToStep(steps[3])}
                            style={style}
                            token={token} />;
            case "CONFIRMATION": 
                return <ConfirmStep 
                            taskData={localTaskData}
                            event = {event} 
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