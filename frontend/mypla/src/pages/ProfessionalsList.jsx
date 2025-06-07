import './styles/ProfessionalsList.css';
import React, { useEffect, useState } from 'react';
import { getProfessionalsByTopic } from '../services/professionals-topic/professionals-topic.service';
import { useSearchParams } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from 'react-router-dom';


export const ProfessionalsList = ({ token }) => {
    
    const [searchParams] = useSearchParams();
    const topic = searchParams.get("topic");
    const [profs, setProfs] = useState([]);
    const { isAuthenticated } = useAuth0();
    const navigate = useNavigate();
    
    useEffect(() => {
        const cargarProfesionales = async () => {
            try {
                const data = await getProfessionalsByTopic(token, topic);
                setProfs(data);
            } catch (error) {
                console.error("Error al obtener profesionales:", error);
            }
        };
        if (isAuthenticated && topic) {
            cargarProfesionales();
        }
    }, [topic, isAuthenticated]);
    
    useEffect(() => {
        // Eliminar tabla anterior
        $("#profs-table").remove();
        
        // Crear nueva tabla
        const tabla = $(`
            <table id="profs-table">
            <thead>
            <tr>
            <th class="username">Nombre</th>
            <th class="score">Puntuacion</th>
            <th class="price">Precio/hr</th>
            </tr>
            </thead>   
            <tbody></tbody>
            </table>
            `);
            
            for (let prof of profs) {
                const fila = $(`
                    <tr>
                    <td>${prof.username}</td>
                    <td>${prof.score}</td>
                    <td>$ ${prof.price_class}</td>
                    </tr>
                    `);
                    
                fila.on('click', () => {
                    navigate(`/calendar/${encodeURIComponent(prof.prof_id)}`)
                });

                tabla.find("tbody").append(fila);
            }

        $("#table-container").append(tabla);
    }, [profs]);

    return (
        <div id='gral-table-container'>
            <div id="table-title-container">
                <h2>Profesionales para el tópico: <span>{topic}</span></h2>
            </div>
            <div id="table-container"></div>
        </div>
    );
};