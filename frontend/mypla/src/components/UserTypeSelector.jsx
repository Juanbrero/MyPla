// src/components/UserTypeSelector.js

import React, { useState } from "react";

export const UserTypeSelector = ({ onUserTypeSelected }) => {
  const [selectedType, setSelectedType] = useState("");

  const handleSelect = (e) => {
    setSelectedType(e.target.value);
    onUserTypeSelected(e.target.value); 
  };

  return (
    <div>
      <label>
        <input
          type="radio"
          value="alumno"
          checked={selectedType === "alumno"}
          onChange={handleSelect}
        />
        Alumno
      </label>
      <label>
        <input
          type="radio"
          value="profesional"
          checked={selectedType === "profesional"}
          onChange={handleSelect}
        />
        Profesional
      </label>
    </div>
  );
};
