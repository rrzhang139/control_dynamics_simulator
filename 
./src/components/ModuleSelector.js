import React from 'react';

// ModuleSelector component allows users to choose which simulation module to display
const ModuleSelector = ({ 
  currentModule, 
  onModuleChange, 
  modules 
}) => {
  // Handle module selection change
  const handleModuleChange = (e) => {
    onModuleChange(e.target.value);
  };

  return (
    <div className="module-selector">
      <h3>Select Simulation Module</h3>
      <select 
        value={currentModule} 
        onChange={handleModuleChange}
        className="module-select"
      >
        {modules.map(module => (
          <option key={module.id} value={module.id}>
            {module.name}
          </option>
        ))}
      </select>
      <p className="module-description">
        {modules.find(m => m.id === currentModule)?.description || ''}
      </p>
    </div>
  );
};

export default ModuleSelector;

