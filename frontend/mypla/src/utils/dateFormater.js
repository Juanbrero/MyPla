

export const dateFormater = (input) => {

    const [datePart, timePart] = input.split("T");
    const [hours, minutes] = timePart.split(":");

    const formatted = `${hours}:${minutes}:00.469Z`;

    return formatted;
}