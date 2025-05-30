import React, { useContext, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import { TutorialContext } from './TutorialContext';
import './TutorialGuide.css';

const steps = [
  { title: 'Bienvenido a nuestra plataforma!', 
    content: 'Recordá que es un work in progress.',
    foot: 'Hagamos un recorrido ->', 
    selector: '' },

  { title: 'Log in / Sing up', 
    content: 'La gestion del modulo de usuarios esta realizada integrando Auth0, con autenticacion de doble factor, y usando su capacidad de gestion de roles.', 
    foot: 'Logueate para seguir ->',
    selector: '.loginButtons' },

  { title: 'Calendario', 
    content: 'Vamos a ver como se vería la funcionalidad de calendario para el tipo de usuario que seleccionaste.', 
    foot: '',
    selector: '.fc' },

  { title: 'aaa', 
    content: 'aaa', 
    foot: 'aaa',
    selector: '' },
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

    if (!isOpen) return; // si está cerrado, no hacemos nada

    const selector = steps[stepIndex]?.selector;
    if (!selector) return;

    const element = document.querySelector(selector);
    if (element) {
      element.classList.add('highlight-tutorial');
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
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
