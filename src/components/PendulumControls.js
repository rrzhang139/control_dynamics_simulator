import React from 'react';

// Component for controlling pendulum simulation parameters
const PendulumControls = ({ params, onParamChange, paused, onTogglePause, onReset }) => {
  // Handle slider input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    onParamChange({
      ...params,
      [name]: parseFloat(value)
    });
  };

  // Reset to initial state
  const handleReset = () => {
    onReset();
  };

  return (
    <div className="pendulum-controls">
      <h3>Pendulum Parameters</h3>
      
      <div className="control-group">
        <label>
          Length (m):
          <input
            type="range"
            name="length"
            min="0.1"
            max="5.0"
            step="0.1"
            value={params.length}
            onChange={handleChange}
          />
          <span className="param-value">{params.length.toFixed(1)}</span>
        </label>
      </div>
      
      <div className="control-group">
        <label>
          Mass (kg):
          <input
            type="range"
            name="mass"
            min="0.1"
            max="10.0"
            step="0.1"
            value={params.mass}
            onChange={handleChange}
          />
          <span className="param-value">{params.mass.toFixed(1)}</span>
        </label>
      </div>
      
      <div className="control-group">
        <label>
          Gravity (m/s²):
          <input
            type="range"
            name="gravity"
            min="0"
            max="20"
            step="0.5"
            value={params.gravity}
            onChange={handleChange}
          />
          <span className="param-value">{params.gravity.toFixed(1)}</span>
        </label>
      </div>
      
      <div className="control-group">
        <label>
          Damping:
          <input
            type="range"
            name="damping"
            min="0"
            max="2"
            step="0.05"
            value={params.damping}
            onChange={handleChange}
          />
          <span className="param-value">{params.damping.toFixed(2)}</span>
        </label>
      </div>
      
      <div className="control-group">
        <label>
          Initial Angle (degrees):
          <input
            type="range"
            name="initialAngle"
            min={-Math.PI}
            max={Math.PI}
            step="0.1"
            value={params.initialAngle}
            onChange={handleChange}
          />
          <span className="param-value">
            {Math.round(params.initialAngle * 180 / Math.PI)}°
          </span>
        </label>
      </div>
      
      <div className="control-buttons">
        <button onClick={onTogglePause} className="control-button">
          {paused ? 'Start' : 'Pause'}
        </button>
        
        <button onClick={handleReset} className="control-button">
          Reset
        </button>
      </div>
      
      <div className="pendulum-info">
        <h4>About Double Integrator</h4>
        <p>
          A double integrator calculates position by integrating velocity, 
          which is itself calculated by integrating acceleration.
        </p>
        <p>
          For a pendulum, the equation of motion is:
          <br />
          α = -g/L × sin(θ) - b×ω
        </p>
        <p>
          Where:<br />
          α = angular acceleration<br />
          g = gravity<br />
          L = length<br />
          θ = angle<br />
          b = damping<br />
          ω = angular velocity
        </p>
      </div>
    </div>
  );
};

export default PendulumControls;

