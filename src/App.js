import React, { useState } from 'react';
import './App.css';
import Pendulum from './components/Pendulum';
import PendulumControls from './components/PendulumControls';

function App() {
  // State to control pendulum parameters
  // Default parameters for reset function
  const defaultParams = {
    length: 1.0,       // Length in meters
    mass: 1.0,         // Mass in kg
    gravity: 9.8,      // Gravity in m/s²
    damping: 0.1,      // Damping coefficient
    initialAngle: Math.PI / 4  // Initial angle in radians (45 degrees)
  };
  
  const [pendulumParams, setPendulumParams] = useState(defaultParams);
  
  // Creating a key that changes when parameters change to force remount
  const [paramChangeCounter, setParamChangeCounter] = useState(0);

  // State to control paused/running simulation
  const [paused, setPaused] = useState(false);

  // Update parameters from user input
  const handleParamChange = (newParams) => {
    // Merge the new params with existing params to ensure all updates are applied
    setPendulumParams(prevParams => ({
      ...prevParams,
      ...newParams
    }));
    
    // Increment the counter to force Pendulum component to remount
    setParamChangeCounter(prev => prev + 1);
  };

  // Toggle pause/resume simulation
  const handleTogglePause = () => {
    setPaused(!paused);
  };

  // Reset simulation
  const handleReset = () => {
    // Reset all parameters to default values
    setPendulumParams(defaultParams);
    
    // Increment the counter to force Pendulum component to remount
    setParamChangeCounter(prev => prev + 1);
    
    // Restart animation if paused
    if (paused) {
      setPaused(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Pendulum Double Integrator Simulation</h1>
      </header>
      
      <div className="simulation-container">
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
      </div>
    </div>
  );
}

export default App;
