export const dateFormater = (input) => {

    console.log("input: ", input);
    const [datePart, timePart] = input.split("T");
    console.log(timePart);
    const [hours, minutes] = timePart.split(":");
    // console.log(timePart);

    const formatted = `${hours}:${minutes}:00.469Z`;

    return formatted;
}

export const dateFormaterReverse = (date, time) => {
    const [hours, minutes] = time.split(":");

    return `${date}T${hours}:${minutes}`;
    // formato: '2025-05-29T01:00'
}

export const dateObjToLocalTime = (dateObj) => {
    const date = `${dateObj.getFullYear()}-${(dateObj.getMonth()+1).toString().padStart(2, '0')}-${dateObj.getDate().toString().padStart(2, '0')}`;
    const time = `${dateObj.getHours().toString().padStart(2, '0')}:${dateObj.getMinutes().toString().padStart(2, '0')}`;

    return dateFormaterReverse(date, time);

}

export const stringDateToLocalTime = (dateString) => {
    const [datePart, timePart] = dateString.split("T");

    return timePart;
}