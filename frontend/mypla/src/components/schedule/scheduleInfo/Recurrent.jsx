import * as React from 'react';
import {
  Box, Typography, Checkbox, FormControlLabel
} from '@mui/material';
import { useEffect } from 'react'

export default function ScheduleTime(props) {
    const { taskData, isEditable } = props;

    const [isRecurring, setIsRecurring] = React.useState(taskData?.recurrent || false);


    useEffect(() => {
    
        setIsRecurring(taskData?.recurrent || false);
    
    }, [taskData?.recurrent]);
    

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
                       onChange={(e) => setIsRecurring(e.target.checked)}
                    />
                }
                label="Repetir semanalmente"
               sx={{ mt: 2 }}
            />
           )}
        </>
    )

}