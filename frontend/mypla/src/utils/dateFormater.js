export const dateFormater = (input) => {

    const [datePart, timePart] = input.split("T");
    const [hours, minutes] = timePart.split(":");

    const formatted = `${hours}:${minutes}:00.469Z`;

    return formatted;
}

export const dateFormaterReverse = (date, time) => {
    const [hours, minutes] = time.split(":");

    return `${date}T${hours}:${minutes}`;
    // formato: '2025-05-29T01:00'
}