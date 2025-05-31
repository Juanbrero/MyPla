import * as React from 'react';
import {
  Box, Typography, Checkbox, FormControlLabel
} from '@mui/material';
import { useEffect } from 'react'

export default function ScheduleTime(props) {
   
    const { taskData, clickedEvent, isEditable, onChangeData } = props;

    const [isRecurring, setIsRecurring] = React.useState(taskData?.category === "recurrent");
    const [editRecurrent, setEditRecurrent] = React.useState(clickedEvent?.extendedProps?.category === "recurrent");
    

    useEffect(() => {
      
        setIsRecurring(taskData?.category === "recurrent");  
        setEditRecurrent(clickedEvent?.extendedProps?.category === "recurrent");  
    
    }, [taskData?.category, clickedEvent?.extendedProps?.category]);
    

    const handleRecurrentChange = (event) => {
        const { target: { checked } } = event;
        setIsRecurring(checked)
        onChangeData?.({ category : checked ? "recurrent" : clickedEvent?.extendedProps?.category});
        // onChangeData?.({ recurrent : checked});
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