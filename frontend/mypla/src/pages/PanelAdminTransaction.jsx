import './styles/PanelAdminTransaction.css';
import { useEffect, useState } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import '@fortawesome/fontawesome-free/css/all.min.css';
import { getPayPending, putRefundPending, putPayPending } from '../services/payments/payment.service';
import PaymentInfoModal from '../components/PaymentInfoModal';


export const PanelAdminTransaction = ({ token }) => {
    
    const [transfer, setTransfer] = useState([]);
    const { isAuthenticated } = useAuth0();
    const [modalOpen, setModalOpen] = useState(false);
    const [selectedRow, setSelectedRow] = useState(null);

    useEffect(() => {
        const cargarTransacciones = async () => {
            try {
                const data = await getPayPending(token);
                setTransfer(data);
            } catch (error) {
                console.error("Error al obtener transacciones:", error);
            }
        };
        if (isAuthenticated) {
            cargarTransacciones();
        }
    }, [isAuthenticated]);
    
    useEffect(() => {
        // Eliminar tabla anterior
        $("#transaction-table").remove();
        
        // Crear nueva tabla
        const tabla = $(`
            <table id="transaction-table">
                <thead>
                    <tr>
                        <th class="emite">Alumno</th>
                        <th class="concepto">Concepto</th>
                        <th class="recibe">Profesional</th>
                        <th class="monto">Monto</th>
                        <th class="fecha">Fecha</th>
                        <th class="estado">Estado</th>
                    </tr>
                </thead>   
                <tbody></tbody>
            </table>
            `);
            
            for (let pay of transfer) {

                const concept = pay.type == "refund" ? "Reembolso" : "Reserva";
                const idBttn = "doneBttn" + transfer.indexOf(pay);
                const transferWay = pay.type == "refund" ? '<i class="fa-solid fa-arrow-left"></i>' : '<i class="fa-solid fa-arrow-right"></i>';
                const payDate = pay.type == "pay" ? new Date(pay.day_hour).toLocaleDateString() : new Date(pay.day_hour_cancel).toLocaleDateString();

                const fila = $(`
                    <tr id=tr-${transfer.indexOf(pay)} class=tr-${concept}>
                        <td id="payId" class="td-oculto"> ${transfer.indexOf(pay)} </td>
                        <td id="payAddress" class="td-oculto"> ${pay.cvu} </td>
                        <td id="payAlum">${pay.user_student.email}</td>
                        <td>
                            <div id="type-cell">
                                <p id="payConcept">${concept}</p>
                                <span>${transferWay}</span>
                            </div>
                        </td>
                        <td id="payProf">${pay.user_professional.email}</td>
                        <td id="payAmount">$ ${pay.price}</td>
                        <td id="payDate">${payDate}</td>
                        <td id="td-button"><button id=${idBttn}>Hecho</button></td>
                    </tr>
                    `);
                    
                fila.on('click', function () {
                    const data = {
                        id: $(this).find("#payId").text(),
                        address: $(this).find("#payAddress").text(),
                        alum: $(this).find("#payAlum").text(),
                        prof: $(this).find("#payProf").text(),
                        concept: $(this).find("#payConcept").text(),
                        amount: $(this).find("#payAmount").text(),
                        date: $(this).find("#payDate").text(),
                    };
                    setSelectedRow(data);
                    setModalOpen(true);
                });

                // Evita que el click del botón dispare el del <tr>
                fila.find(`#${idBttn}`).on('click', async (e) => {
                    e.stopPropagation();

                    if(pay.type == "pay") {
                        await putPayPending(token, pay);
                    }
                    else {
                        await putRefundPending(token, pay);
                    }

                    // Reemplazar el botón por texto "Confirmado"
                    const boton = $(e.currentTarget);
                    boton.replaceWith('<span class="confirmado">Confirmado</span>');
                });

                tabla.find("tbody").append(fila);
                
            }

        $("#table-transaction-container").append(tabla);
    }, [transfer]);

    return (
        <div id='gral-transaction-table-container'>
            <div id="table-transaction-title-container">
                <h2>Transacciones pendientes</h2>
            </div>
            <div id="table-transaction-container"></div>
            <PaymentInfoModal 
                paymentRow={selectedRow}
                open={modalOpen}
                onClose={() => setModalOpen(false)}
            />
        </div>

    );

}