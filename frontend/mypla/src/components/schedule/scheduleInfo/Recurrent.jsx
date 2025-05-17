import * as React from 'react';
import {
  Box, Typography, Checkbox, FormControlLabel
} from '@mui/material';
import { useEffect } from 'react'

export default function ScheduleTime(props) {
   
    const { taskData, clickedEvent, isEditable, onChangeData } = props;

    const [isRecurring, setIsRecurring] = React.useState(taskData?.recurrent || false);
    const [editRecurrent, setEditRecurrent] = React.useState(clickedEvent?.recurrent);
    

    useEffect(() => {
    
        setIsRecurring(taskData?.recurrent || false);
        setEditRecurrent(clickedEvent?.recurrent);
    
    }, [taskData?.recurrent, clickedEvent?.recurrent]);
    

    const handleRecurrentChange = (event) => {
        const { target: { checked } } = event;
        setIsRecurring(checked)
        onChangeData?.({ recurrent : checked});
    };
    return (
        <>
        {!isEditable ? (
            <Box>
                <Typography variant="subtitle1">
                    <strong>Es recurrente:</strong> {editRecurrent ? 'Sí' : 'No'}
                </Typography>
            </Box>
        ) : (
            <FormControlLabel
               control={
                    <Checkbox
                       checked={isRecurring}
                       onChange={handleRecurrentChange}
                    />
                }
                label="Repetir semanalmente"
               sx={{ mt: 2 }}
            />
           )}
        </>
    )

}