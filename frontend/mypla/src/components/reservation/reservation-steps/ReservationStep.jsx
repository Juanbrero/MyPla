import { Box, Button, Typography } from '@mui/material';
import ScheduleDate from '../../shedule/schedule-components/ScheduleDate';
import ScheduleTime from '../../shedule/schedule-components/ScheduleTime';
import ScheduleTopics from '../../shedule/schedule-components/ScheduleTopics';


export default function ReservationStep({ taskData, onClose, onNext, style}) {

    return (
        <Box sx={style}>
                <Typography variant="h6" mb={2}>
                    Realizar reserva
                </Typography>
                
                <ScheduleTopics
                    value={taskData?.topics || []}
                    topicsList={taskData?.avaliableTopics}
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