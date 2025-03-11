import React from 'react';

// SimulationWrapper component acts as a container for different simulation modules
const SimulationWrapper = ({ 
  moduleType, 
  moduleParams, 
  paused, 
  paramChangeCounter 
}) => {
  // Dynamically import the correct module based on moduleType
  const renderModule = () => {
    switch (moduleType) {
      case 'pendulum':
        // Import the Pendulum module
        const Pendulum = require('./Pendulum').default;
        return (
          <Pendulum
            key={`pendulum-${paramChangeCounter}`}
            params={moduleParams}
            paused={paused}
          />
        );
      case 'pendulum-control':
        // Import the PendulumControl module
        const PendulumControl = require('./PendulumControl').default;
        return (
          <PendulumControl
            key={`pendulum-control-${paramChangeCounter}`}
            params={moduleParams}
            paused={paused}
          />
        );
      default:
        return <div>Please select a simulation module</div>;
    }
  };

  return (
    <div className="simulation-wrapper">
      {renderModule()}
    </div>
  );
};

export default SimulationWrapper;

