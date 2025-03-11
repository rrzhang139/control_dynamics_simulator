import React from 'react';

// Component for selecting which simulation module to display
const ModuleSelector = ({ activeModule, onModuleChange }) => {
  return (
    <div className="module-selector">
      <h3>Select Simulation</h3>
      <div className="module-buttons">
        <button
          className={`module-button ${activeModule === 'pendulum' ? 'active' : ''}`}
          onClick={() => onModuleChange('pendulum')}
        >
          Simple Pendulum
        </button>
        
        <button
          className={`module-button ${activeModule === 'pendulum-control' ? 'active' : ''}`}
          onClick={() => onModuleChange('pendulum-control')}
        >
          Controlled Pendulum
        </button>
      </div>
    </div>
  );
};

export default ModuleSelector;

