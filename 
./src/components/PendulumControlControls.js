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
      <h3>Controlled Pendulum Parameters</h3>
      
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
            value={params

