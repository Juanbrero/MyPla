import React, { useEffect, useState } from 'react';
import { getProfessionalsByTopic } from '../services/professionals-topic/professionals-topic.service';
import { useSearchParams } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";

export const ProfessionalsList = ({ token }) => {
    
    const [searchParams] = useSearchParams();
    const topic = searchParams.get("topic");
    const [profs, setProfs] = useState([]);
    const { isAuthenticated } = useAuth0();

        useEffect(() => {
        const cargarProfesionales = async () => {
            try {
                const data = await getProfessionalsByTopic(token, topic);
                console.log(data);
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
        $("#tabla_profs").remove();

        // Crear nueva tabla
        const tabla = $(`
            <table id="tabla_profs" style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Precio</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        `);

        for (let prof of profs) {
            const fila = $(`
                <tr>
                    <td>${prof.prof_id}</td>
                    <td>${prof.price_class}</td>
                </tr>
            `);
            tabla.find("tbody").append(fila);
        }

        $("#contenedor-tabla").append(tabla);
    }, [profs]);

    return (
        <div>
            <h2>Profesionales para el tópico: {topic}</h2>
            <div id="contenedor-tabla"></div>
        </div>
    );
};