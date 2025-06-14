import Calendario from "../shedule/Calendario";
import StudentMyCalendar from "../studentMyCalendar/StudentMyCalendar";

const CalendarioWrapper = ({token, roles}) => {
  if (roles.includes("Profesional")) {
    return <Calendario token={token} />;
  }

  if (roles.includes("Alumno")) {
    return <StudentMyCalendar token={token} />;
  }

  return <div>Loggueate antes de ingresar</div>;
};

export default CalendarioWrapper;
