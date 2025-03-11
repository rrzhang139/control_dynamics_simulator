import React from 'react';

// Component for controlling pendulum control simulation parameters
const PendulumControlControls = ({ params, onParamChange, paused, onTogglePause, onReset }) => {
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
      <h3>Pendulum Control Parameters</h3>
      
      {/* Physical Parameters */}
      <div className="parameter-section">
        <h4>Physical Parameters</h4>
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
      </div>

      {/* Control Parameters */}
      <div className="parameter-section">
        <h4>Control Parameters</h4>
        <div className="control-group">
          <label>
            Kp (Proportional Gain):
            <input
              type="range"
              name="kp"
              min="0"
              max="50"
              step="0.5"
              value={params.kp}
              onChange={handleChange}
            />
            <span className="param-value">{params.kp.toFixed(1)}</span>
          </label>
        </div>
        
        <div className="control-group">
          <label>
            Kd (Derivative Gain):
            <input
              type="range"
              name="kd"
              min="0"
              max="20"
              step="0.5"
              value={params.kd}
              onChange={handleChange}
            />
            <span className="param-value">{params.kd.toFixed(1)}</span>
          </label>
        </div>
        
        <div className="control-group">
          <label>
            Energy Gain:
            <input
              type="range"
              name="energyGain"
              min="0"
              max="30"
              step="0.5"
              value={params.energyGain}
              onChange={handleChange}
            />
            <span className="param-value">{params.energyGain.toFixed(1)}</span>
          </label>
        </div>
        
        <div className="control-group">
          <label>
            Torque Limit:
            <input
              type="range"
              name="torqueLimit"
              min="0.1"
              max="10.0"
              step="0.1"
              value={params.torqueLimit}
              onChange={handleChange}
            />
            <span className="param-value">{params.torqueLimit.toFixed(1)}</span>
          </label>
        </div>
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
        <h4>About Pendulum Control</h4>
        <p>
          This simulation implements energy-based swing-up control with PD stabilization.
        </p>
        <p>
          For swing-up (far from upright): Energy injection control is used.<br />
          For stabilization (near upright): PD control is used.
        </p>
        <p>
          The control law switches based on the angle difference from the target.
        </p>
      </div>
    </div>
  );
};

export default PendulumControlControls;

