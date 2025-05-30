// TutorialContext.js
import React, { createContext, useState, useEffect } from 'react';

export const TutorialContext = createContext();

export const TutorialProvider = ({ children }) => {
  const [isOpen, setIsOpen] = useState(() => {
    // Cargar estado inicial de localStorage
    const saved = localStorage.getItem('tutorialIsOpen');
    return saved ? JSON.parse(saved) : false;
  });
  const [stepIndex, setStepIndex] = useState(() => {
    const saved = localStorage.getItem('tutorialStepIndex');
    return saved ? Number(saved) : 0;
  });

  useEffect(() => {
    localStorage.setItem('tutorialIsOpen', JSON.stringify(isOpen));
  }, [isOpen]);

  useEffect(() => {
    localStorage.setItem('tutorialStepIndex', stepIndex);
  }, [stepIndex]);

  return (
    <TutorialContext.Provider value={{ isOpen, setIsOpen, stepIndex, setStepIndex }}>
      {children}
    </TutorialContext.Provider>
  );
};
