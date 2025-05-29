import { dateFormaterReverse } from "../../utils/dateFormater";
import { callExternalApi } from "../external-api.service";

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;
const dias = ['', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

export const getAvailableProfessional = async (prof_id, token) => {

    const config = {
    url: `${apiServerUrl}/available/professionals?prof_id=${encodeURIComponent(prof_id)}`,
    method: "GET",
    headers: {
        "content-type": "application/json",
        // "Authorization": `Bearer ${token}`,
    }
    };

    const { data, error } = await callExternalApi({ config });

    if (data) {
        for (const category in data) {
            if (data.hasOwnProperty(category)) {
                data[category] = data[category].map(item => {
                    const fecha = new Date(item.day)
                    const diaSemana = fecha.getDay()
                    return {
                        // id        :   arg.event.id,
                        // groupId   :   arg.event?.groupId,
                        // title     :   arg.event.title,
                        // color     :   arg.event.color,
                        start     :   dateFormaterReverse(item.day, item.start),
                        end       :   dateFormaterReverse(item.day, item.end),
                        extendedProps: {
                            day         : item.week_day ? dias[item.week_day] : dias[diaSemana],
                            date        : item.day ? item.day : '',
                            recurrent: category == 'recurrent',
                            eventTopics : item.topics ? item.topics : [],
                        }
                    };
                });
            }
        }
    }
        
    return {
        data: data,
        error,
    };
};