import './styles/PanelAdminTransaction.css';
import { useEffect, useState } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';



export const PanelAdminTransaction = ({ token }) => {
    
    const [transfer, setTransfer] = useState([]);
    const { isAuthenticated } = useAuth0();
    const navigate = useNavigate();
    
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
            
            // for (let tran of transfer) {

            //     const idBttn = "doneBttn" + tran.id;
            //     const fila = $(`
            //         <tr>
            //             <td>${tran.user_student.email}</td>
            //             <td>${tran.type}</td>
            //             <td>${tran.user_professional.email}</td>
            //             <td>$ ${tran.amount}</td>
            //             <td>${tran.date}</td>
            //             <td><button id=${idBttn}>Hecho<button/></td>
            //         </tr>
            //         `);
                    
            //     fila.on('click', () => {
            //         navigate(`/calendar/${encodeURIComponent(tran.prof_id)}`)
            //     });

            //   // Evita que el click del botón dispare el del <tr>
            //      fila.find(`#${idBttn}`).on('click', (e) => {
            //          e.stopPropagation();
            //         alert("chau");
            //      });

            //     tabla.find("tbody").append(fila);
                
            // }

            for (let i=0;i<25;i++) {

                const concept = i%3==0 ? "refund" : "pay";
                const idBttn = "doneBttn" + i;
                const transferWay = concept == "refund" ? '<i class="fa-solid fa-arrow-left"></i>' : '<i class="fa-solid fa-arrow-right"></i>';
                const fila = $(`
                    <tr class=tr-${concept}>
                        <td>juaan.b17@hotmail.com</td>
                        <td>
                            <div id="type-cell">
                                <p>${concept}</p>
                                <span>${transferWay}</span>
                            </div>    
                        </td>
                        <td>juaan.b18@hotmail.com</td>
                        <td>$ 15000</td>
                        <td>12/10/2025</td>
                        <td id="td-button"><button id=${idBttn}>Hecho</button></td>
                    </tr>
                    `);
                    
                fila.on('click', () => {
                    alert("hola");
                });

                
                // Evita que el click del botón dispare el del <tr>
                fila.find(`#${idBttn}`).on('click', (e) => {
                    e.stopPropagation();
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
        </div>
    );

}