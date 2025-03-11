import React, { useState } from 'react';
import './App.css';
import Pendulum from './components/Pendulum';
import PendulumControls from './components/PendulumControls';
import PendulumControl from './components/PendulumControl';
import PendulumControlControls from './components/PendulumControlControls';
import ModuleSelector from './components/ModuleSelector';

function App() {
  // State to track which module is active
  const [activeModule, setActiveModule] = useState('pendulum');

  // Default parameters for simple pendulum reset function
  const defaultPendulumParams = {
    length: 1.0,       // Length in meters
    mass: 1.0,         // Mass in kg
    gravity: 9.8,      // Gravity in m/s²
    damping: 0.1,      // Damping coefficient
    initialAngle: Math.PI / 4  // Initial angle in radians (45 degrees)
  };
  
  // Default parameters for controlled pendulum reset function
  const defaultControlledPendulumParams = {
    length: 1.0,       // Length in meters
    mass: 1.0,         // Mass in kg
    gravity: 9.8,      // Gravity in m/s²
    damping: 0.1,      // Damping coefficient
    initialAngle: Math.PI / 16,  // Initial angle in radians (11.25 degrees)
    kp: 5.0,           // Proportional gain for stabilization
    kd: 10.0,           // Derivative gain for stabilization
    energyGain: 10.0,  // Energy control gain
    targetAngle: Math.PI,  // Target angle (π = upright)
    torqueLimit: 1.0   // Maximum torque
  };
  
  // Separate state for each module type
  const [pendulumParams, setPendulumParams] = useState(defaultPendulumParams);
  const [controlledPendulumParams, setControlledPendulumParams] = useState(defaultControlledPendulumParams);
  
  // Creating a key that changes when parameters change to force remount
  const [paramChangeCounter, setParamChangeCounter] = useState(0);

  // State to control paused/running simulation
  const [paused, setPaused] = useState(false);

  // Update parameters from user input based on active module
  const handleParamChange = (newParams) => {
    if (activeModule === 'pendulum') {
      // Update simple pendulum parameters
      setPendulumParams(prevParams => ({
        ...prevParams,
        ...newParams
      }));
    } else if (activeModule === 'pendulum-control') {
      // Update controlled pendulum parameters
      setControlledPendulumParams(prevParams => ({
        ...prevParams,
        ...newParams
      }));
    }
    
    // Increment the counter to force component to remount
    setParamChangeCounter(prev => prev + 1);
  };

  // Handle module change
  const handleModuleChange = (moduleType) => {
    setActiveModule(moduleType);
    // Reset the param change counter to force remount of new module
    setParamChangeCounter(prev => prev + 1);
  };

  // Toggle pause/resume simulation
  const handleTogglePause = () => {
    setPaused(!paused);
  };

  // Reset simulation based on active module
  const handleReset = () => {
    // Reset parameters to default values based on active module
    if (activeModule === 'pendulum') {
      setPendulumParams(defaultPendulumParams);
    } else if (activeModule === 'pendulum-control') {
      setControlledPendulumParams(defaultControlledPendulumParams);
    }
    
    // Increment the counter to force component to remount
    setParamChangeCounter(prev => prev + 1);
    
    // Restart animation if paused
    if (paused) {
      setPaused(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Control Dynamics Simulator</h1>
      </header>
      
      <ModuleSelector 
        activeModule={activeModule}
        onModuleChange={handleModuleChange}
      />
      
      <div className="simulation-container">
        {/* Conditionally render the appropriate simulation module */}
        {activeModule === 'pendulum' ? (
          <>
            <Pendulum 
              key={`pendulum-${paramChangeCounter}`}
              params={pendulumParams} 
              paused={paused} 
            />
            
            <PendulumControls 
              params={pendulumParams}
              onParamChange={handleParamChange}
              paused={paused}
              onTogglePause={handleTogglePause}
              onReset={handleReset}
            />
          </>
        ) : activeModule === 'pendulum-control' ? (
          <>
            <PendulumControl 
              key={`pendulum-control-${paramChangeCounter}`}
              params={controlledPendulumParams} 
              paused={paused} 
            />
            
            <PendulumControlControls 
              params={controlledPendulumParams}
              onParamChange={handleParamChange}
              paused={paused}
              onTogglePause={handleTogglePause}
              onReset={handleReset}
            />
          </>
        ) : null}
      </div>
    </div>
  );
}

export default App;
