import './styles/PanelAdminTransaction.css';
import { useEffect, useState } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import '@fortawesome/fontawesome-free/css/all.min.css';
import { getPayPending, putRefundPending, putPayPending } from '../services/payments/payment.service';
import PaymentInfoModal from '../components/PaymentInfoModal';



export const PanelAdminTransaction = ({ token }) => {
    
    const [transfer, setTransfer] = useState(
        [
            {
                "id": 1,
                "type": "pay",
                "amount": 11111,
                "CVU": 11,
                "fecha": "11/11/1111",
                "user_student": {
                    "student_id": "11111",
                    "email": "111111"
                },
                "user_professional": {
                    "professional_id": "22222",
                    "email": "2222"
                }
            },
            {
                "id": 2,
                "type": "refund",
                "amount": 11111,
                "CVU": 22,
                "fecha": "22/22/2222",
                "user_student": {
                    "student_id": "11111",
                    "email": "11111"
                },
                "user_professional": {
                    "professional_id": "22222",
                    "email": "22222"
                }
            },
            {
                "id": 3,
                "type": "refund",
                "amount": 3333,
                "CVU": 33333,
                "fecha": "3/3/2333",
                "user_student": {
                    "student_id": "3333",
                    "email": "3333"
                },
                "user_professional": {
                    "professional_id": "4444",
                    "email": "44444"
                }
            },
            {
                "id": 4,
                "type": "pay",
                "amount": 5555,
                "CVU": 5555,
                "fecha": "5/5/5555",
                "user_student": {
                    "student_id": "555",
                    "email": "5555"
                },
                "user_professional": {
                    "professional_id": "6666",
                    "email": "6666"
                }
            },
            {
                "id": 5,
                "type": "pay",
                "amount": 77777,
                "CVU": 7777, 
                "fecha": "77/77/7777",
                "user_student": {
                    "student_id": "7777",
                    "email": "7777"
                },
                "user_professional": {
                    "professional_id": "8888",
                    "email": "88888"
                }
            }
        ]
    );
    const { isAuthenticated } = useAuth0();
    const [modalOpen, setModalOpen] = useState(false);
    const [selectedRow, setSelectedRow] = useState(null);

    useEffect(() => {
        const cargarTransacciones = async () => {
            try {
                // const data = await getPayPending(token);
                // setTransfer(data);
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
                const idBttn = "doneBttn" + pay.id;
                const transferWay = pay.type == "refund" ? '<i class="fa-solid fa-arrow-left"></i>' : '<i class="fa-solid fa-arrow-right"></i>';
                const fila = $(`
                    <tr id=tr-${pay.id} class=tr-${concept}>
                        <td id="payId" class="td-oculto"> ${pay.id} </td>
                        <td id="payAddress" class="td-oculto"> ${pay.CVU} </td>
                        <td id="payAlum">${pay.user_student.email}</td>
                        <td>
                            <div id="type-cell">
                                <p id="payConcept">${concept}</p>
                                <span>${transferWay}</span>
                            </div>
                        </td>
                        <td id="payProf">${pay.user_professional.email}</td>
                        <td id="payAmount">$ ${pay.amount}</td>
                        <td id="payDate">${pay.fecha}</td>
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