import * as React from 'react';
import {
  Box, Typography, Checkbox, FormControlLabel
} from '@mui/material';
import { useEffect } from 'react'

export default function ScheduleTime(props) {
    const { taskData, isEditable, onChangeData } = props;

    const [isRecurring, setIsRecurring] = React.useState(taskData?.recurrent || false);


    useEffect(() => {
    
        setIsRecurring(taskData?.recurrent || false);
    
    }, [taskData?.recurrent]);
    

    const handleRecurrentChange = (event) => {
        const { target: { checked } } = event;
        setIsRecurring(checked)
        onChangeData?.({ recurrent : checked});
    };
    return (
        <>
        {!isEditable ? (
            <Box>
                <Typography variant="subtitle1"><strong>Es recurrente:</strong> {isRecurring ? 'Sí' : 'No'}</Typography>
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