import './colorReferenceHelp.css'

export const ColorReferenceHelp = () => {

    return (
        <div className="color-ref-container">
          <ul className="color-list">
            <li className="green" data-tooltip="Horario que se repite solo una vez en una fecha específica">Horario especifico</li>
            <li className="blue" data-tooltip="Horario que se repite regularmente (ej: todos los lunes)">Horario recurrente</li>
            <li className="orange" data-tooltip="Horario creado para cancelar una franja horaria de un horario recurrente, en una fecha en particular.">Horario excepcion</li>
          </ul>
        </div>
    )
}