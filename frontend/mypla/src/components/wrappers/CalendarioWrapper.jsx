import Calendario from "../shedule/Calendario";
import StudentCalendar from "../studentCalendar/StudentCalendar";

const CalendarioWrapper = ({token, roles}) => {
  if (roles.includes("Profesional")) {
    return <Calendario token={token} />;
  }

  if (roles.includes("Alumno")) {
    return <StudentCalendar token={token} />;
  }

  return <div>Loggueate antes de ingresar</div>;
};

export default CalendarioWrapper;
