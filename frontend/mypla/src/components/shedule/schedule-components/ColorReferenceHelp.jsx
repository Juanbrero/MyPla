import './colorReferenceHelp.css'

export const ColorReferenceHelp = () => {

    return (
        <div className="color-ref-container">
          <ul className="color-list">
            <li className="green">Horario especifico</li>
            <li className="blue">Horario recurrente</li>
            <li className="orange">Horario excepcion</li>
          </ul>
        </div>
    )
}