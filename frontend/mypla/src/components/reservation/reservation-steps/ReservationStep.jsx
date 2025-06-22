import { Box, Button, Typography } from '@mui/material';
import ScheduleDate from '../../shedule/schedule-components/ScheduleDate';
import ScheduleTime from '../../shedule/schedule-components/ScheduleTime';
import ScheduleTopicsReservation from '../ScheduleTopicsReservation';


export default function ReservationStep({ taskData, event, onClose, onNext, style}) {
    return (
        <Box sx={style}>
                <Typography variant="h6" mb={2}>
                    Realizar reserva
                </Typography>
                
                {taskData ? (
                    <>
                        <ScheduleTopicsReservation
                        value={taskData?.selectedTopic || ''} // más claro y directo
                        isEditable={false}
                        />
                        <ScheduleDate
                        type={'specific'}
                        value={{ week_day: taskData?.week_day, date: taskData?.day }}
                        isEditable={false}
                        />
                        <ScheduleTime
                        value={{ start: taskData?.start, end: taskData?.end }}
                        isEditable={false}
                        />
                    </>
                ) : (
                    <>
                        <ScheduleTopicsReservation
                        value={event?.topic || ''}
                        isEditable={false}
                        />
                        
                        <Typography variant="subtitle1">
                            <strong>Anfitrion del evento: </strong>
                            {event?.creator}
                        </Typography>
                        
                        <Typography variant="subtitle1">
                            <strong>Coanfitriones invitados: </strong>
                            {event?.participants?.join(', ')}
                        </Typography>
                        
                        <ScheduleDate
                        type={'specific'}
                        value={{date: event?.date}}
                        isEditable={false}
                        />
                        <ScheduleTime
                        value={{ start: event?.hour, end: null }}
                        isEditable={false}
                        />

                        <Typography variant="subtitle1">
                            <strong>Valor de inscripcion: </strong>
                            $ {event?.precio}
                        </Typography>
                        
                    </>
                )
                }

                {/* Botones */}
                <Box
                    display="flex"
                    justifyContent="flex-end"
                    flexDirection={{ xs: 'column', sm: 'row' }}
                    gap={2}
                    mt={3}
                >       
                    <Button
                        color="secondary"
                        variant="outlined"
                        onClick={() => onClose?.()}
                        fullWidth
                        sx={{ p: 2 }}
                    >
                        Volver
                    </Button>

                    <Button
                        color="primary"
                        variant="contained"
                        onClick={onNext}
                        fullWidth
                        sx={{ p: 2 }}
                    >
                        Reservar
                    </Button>
                </Box>
            </Box>
    );
}