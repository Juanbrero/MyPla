import React, { useContext, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import { TutorialContext } from './TutorialContext';
import './TutorialGuide.css';

const steps = [
  { title: 'Bienvenido a nuestra plataforma!', 
    content: 'Recordá que es un work in progress.',
    foot: 'Hagamos un recorrido ->', 
    selector: '' },
  
  { title: 'Crear cuenta', 
    content: 'Usa el boton para crear una cuenta e iniciar a usar la app arranquemos por un profesional',
    selector: '.button__sign-up' },

  { title: 'Agrega los tópicos de lo que sepas enseñar', 
    content: 'En esta seccion se ve el perfil y podras agregar el topico y precio de la clase',
    selector: '.topic_form' },

  { title: 'Vamos a la agenda', 
    content: 'La gestion del modulo de usuarios esta realizada integrando Auth0, con autenticacion de doble factor, y usando su capacidad de gestion de roles.', 
    foot: 'Clickea la agenda',
    selector: '.agenda-link' },
  
  { title: 'Crea disponibilidad horaria', 
      content: 'Clickeando cualquier celda de la agenda permite crear horarios recurrentes y especificos', 
      selector: '.prof-topics' },
    
  {
    title: 'Salir de la cuenta',
    content: 'Salimos de la cuenta y probemos crear una cuenta de alumno',
    selector: '.logout-link'
  },

  { title: 'Entremos como alumno', 
    content: 'Crea una nueva cuenta como alumno', 
    foot: '',
    selector: '.button__sign-up' },
  
  { title: 'Busca profesionales', 
      content: 'Selecciona un tópico de tu interes', 
      foot: '',
      selector: '.search-container' },
  
  { title: 'Volvamos a la agenda', 
    content: 'Al alumno se le gestiona las clases que tiene reservadas', 
    foot: 'Clickea la agenda',
    selector: '.agenda-link' },

  { 
    title: 'Puede cancelar si quiere la clase', 
    content: 'Puede clickear y cancelar la clase en caso de no poder asistir', 
    foot: '',
    selector: '.celda-specific' 
  },
];


const TutorialGuide = () => {
  const { isOpen, setIsOpen, stepIndex, setStepIndex } = useContext(TutorialContext);
  const popupRef = useRef(null);
  const buttonRef = useRef(null);

  const handleNext = () => {
    if (stepIndex < steps.length - 1) setStepIndex(stepIndex + 1);
  };

  const handlePrev = () => {
    if (stepIndex > 0) setStepIndex(stepIndex - 1);
  };

  const handleToggle = () => setIsOpen(!isOpen);

  useEffect(() => {
    if (!isOpen) return;

    function handleClickOutside(event) {
      if (
        popupRef.current && !popupRef.current.contains(event.target) &&
        buttonRef.current && !buttonRef.current.contains(event.target)
      ) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, setIsOpen, setStepIndex]);

  useEffect(() => {
    // Primero removemos el highlight previo
    document.querySelectorAll('.highlight-tutorial').forEach(el => el.classList.remove('highlight-tutorial'));
    document.querySelectorAll('.highlight-tutorial2').forEach(el => el.classList.remove('highlight-tutorial2'));

    if (!isOpen) return; // si está cerrado, no hacemos nada

    const selector = steps[stepIndex]?.selector;
    if (!selector) return;

    const elements = document.querySelectorAll(selector);
    for (const e of elements) {
      if (selector === '.celda-recurrent' || selector === '.celda-specific') {
        e.classList.add('highlight-tutorial2');
      } else {
        e.classList.add('highlight-tutorial');
      }
      e.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [stepIndex, isOpen]);

  const content = (
    <div className="tutorial-container">
      <button ref={buttonRef} onClick={handleToggle} className="tutorial-toggle-btn">
        {isOpen ? 'Cerrar' : 'Tutorial'}
      </button>

      {isOpen && (
        <div className="tutorial-popup" ref={popupRef}>
          <h2>{steps[stepIndex].title}</h2>
          <p>{steps[stepIndex].content}</p>
          <h4>{steps[stepIndex].foot}</h4>

          <div className="tutorial-nav">
            <button onClick={handlePrev} disabled={stepIndex === 0}>
              Anterior
            </button>
            <button onClick={handleNext} disabled={stepIndex === steps.length - 1}>
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  );

  return ReactDOM.createPortal(content, document.body);

};

export default TutorialGuide;
