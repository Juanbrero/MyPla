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

  { title: 'Mercado Pago', 
    content: 'Este botón es uno de los que se utilizaran para pagar una clase, evento o curso, en caso de usar mercado pago',
    selector: '.mpButton' },

  { title: 'Log in / Sing up', 
    content: 'La gestion del modulo de usuarios esta realizada integrando Auth0, con autenticacion de doble factor, y usando su capacidad de gestion de roles.', 
    foot: 'Logueate para seguir ->',
    selector: '.loginButtons' },
  
  { title: 'Profile', 
      content: 'En esta sección se podrá visualizar al perfil del usuario, donde tambien se puede seleccionar los topicos las clases que puede enseñar el profesional.', 
      selector: '.prof-topics' },
    
  {
    title: 'Ir a Agenda',
    content: 'Usa el link para ver la funcionalidad de la agenda de la página.',
    selector: '.link-agenda'
  },

  { title: 'Calendario', 
    content: 'Llegaste a la funcionalidad principal de la página!!', 
    foot: '',
    selector: '.calendario' },
  
  { title: 'Semana', 
      content: 'Con este boton se puede cambiar de semana.', 
      foot: '',
      selector: '.direccion' },
  
  { 
    title: 'Dias Recurrentes', 
    content: 'Estos horarios representan los que el profesional esta disponible en todas las semanas.', 
    foot: '',
    selector: '.celda-recurrent' 
  },

  { 
    title: 'Dias especificos', 
    content: 'Estas celdas son de dias en especifico que el profesor decide dar clase.', 
    foot: '',
    selector: '.celda-specific' 
  },
  { 
    title: 'Agregar horario', 
    content: 'Bueno ahora agreguemos algun horario, para probar, selecciona un espacio vacío del calendario.', 
  },
  { 
    title: 'Integracion con auth0', 
    content: 'Por último dejamos una ruta para que puedan probar la integración con auth0 en caso de estar logueado entren a /test-auth', 
  }
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
