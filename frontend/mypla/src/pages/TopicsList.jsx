import './styles/TopicsList.css';
import React, { useEffect, useState } from 'react';
import { useSearchParams } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from 'react-router-dom';
import { getTopicsByCategory } from '../services/topics/topics.service';


export const TopicsList = ({ token }) => {
    
    const [searchParams] = useSearchParams();
    const category = searchParams.get("category");
    const [topics, setTopics] = useState([]);
    const { isAuthenticated } = useAuth0();
    const navigate = useNavigate();
    
    useEffect(() => {
        const cargarTopicos = async () => {
            try {
                const data = await getTopicsByCategory(category);
                setTopics(data.data);
            } catch (error) {
                console.error("Error al obtener Topicos:", error);
            }
        };
        if (isAuthenticated && category) {
            cargarTopicos();
        }
    }, [category, isAuthenticated]);
    
    useEffect(() => {
        // Eliminar tabla anterior
        $("#topics-table").remove();
        
        // Crear nueva tabla
        const tabla = $(`
            <table id="topics-table">
                <thead>
                    <tr>
                        <th class="topic-th">Topicos</th>
                    </tr>
                </thead>   
                <tbody></tbody>
            </table>
        `);
            
            for (let top of topics) {
                const fila = $(`
                    <tr>
                        <td>${top}</td>
                    </tr>
                `);
                    
                fila.on('click', () => {
                    navigate(`/ProfessionalsList?topic=${encodeURIComponent(top)}`)
                });

                tabla.find("tbody").append(fila);
            }

        $("#table-container").append(tabla);
    }, [topics]);

    return (
        <div id='gral-table-container'>
            <div id="table-title-container">
                <h2>Topicos para la categoria: <span>{category}</span></h2>
            </div>
            <div id="table-container"></div>
        </div>
    );
};