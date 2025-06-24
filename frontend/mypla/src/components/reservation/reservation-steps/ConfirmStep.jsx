import { Box, Button, Typography } from '@mui/material';
import ScheduleDate from '../../shedule/schedule-components/ScheduleDate';
import ScheduleTime from '../../shedule/schedule-components/ScheduleTime';
import ScheduleTopicsReservation from '../ScheduleTopicsReservation';


export default function ConfirmStep({ taskData, event, onClose, style}) {

    return (
        <Box sx={style}>
            <Typography variant="h5" textAlign={'center'} mb={2}>
                Operacion exitosa!
            </Typography>
            <Typography variant="h6" mb={2}>
                Tu reserva:
            </Typography>
                    
            {taskData ? (
                <>    
                    <ScheduleTopicsReservation
                        value={taskData?.selectedTopic || ''} // más claro y directo
                        topicsList={taskData?.topics || []}
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
                        {event?.invites?.join(', ')}
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
                        $ {event?.price}
                    </Typography>
                    
                </>
            )}


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
                    Cerrar
                </Button>
            </Box>
        </Box>
    );
}