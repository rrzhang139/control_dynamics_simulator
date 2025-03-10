import React, { useRef, useEffect, useState } from 'react';
// math is not used anywhere, so removing the import

// This component handles the physics simulation and rendering of a pendulum
const Pendulum = ({ params, paused }) => {
  const canvasRef = useRef(null);
  const requestRef = useRef(null);
  const previousTimeRef = useRef(0);
  
  // Use refs to track physics values for animation
  // This avoids React's asynchronous state updates during animation
  const physicsRef = useRef({
    theta: params.initialAngle,     // Current angle (radians)
    omega: 0,                       // Angular velocity
    alpha: 0                        // Angular acceleration
  });
  
  // State for UI updates (not used directly in animation calculations)
  const [state, setState] = useState({
    theta: params.initialAngle,     // Current angle (radians)
    omega: 0,                       // Angular velocity
    alpha: 0                        // Angular acceleration
  });
  
  console.log("Pendulum rendered with params:", params);
  console.log("Paused state:", paused);
  // Animation/simulation loop - useCallback to prevent recreating on every render
  const animate = React.useCallback((time) => {
    if (previousTimeRef.current === 0) {
      previousTimeRef.current = time;
      console.log("Animation starting at time:", time);
    }
    
    const deltaTime = (time - previousTimeRef.current) / 1000; // Convert to seconds
    previousTimeRef.current = time;
    
    console.log(`Animation frame: dt=${deltaTime.toFixed(3)}s, paused=${paused}`);
    
    if (!paused) {
      updatePhysics(deltaTime);
    }
    
    renderPendulum();
    requestRef.current = requestAnimationFrame(animate);
  }, [paused, params]); // Include params so animate always has latest values

  // Update physics using double integration
  // Update physics using double integration
  const updatePhysics = React.useCallback((dt) => {
    // Don't update if dt is too large (e.g., if tab was inactive)
    if (dt > 0.1) {
      console.log("Skipping large time step:", dt);
      return;
    }
    
    // Calculate acceleration using pendulum equation of motion
    // For a pendulum: α = -g/L * sin(θ) - b*ω (where b is damping)
    const g = params.gravity;
    const L = params.length;
    const m = params.mass;
    const b = params.damping;
    
    // Get current state from ref (not from React state)
    const { theta, omega } = physicsRef.current;
    
    // Calculate angular acceleration (α)
    const alpha = -g/L * Math.sin(theta) - b/m * omega;
    
    // First integration: velocity = previous velocity + acceleration * dt
    const newOmega = omega + alpha * dt;
    
    // Second integration: position = previous position + velocity * dt
    const newTheta = theta + newOmega * dt;
    
    console.log(`Physics update: θ=${newTheta.toFixed(2)}, ω=${newOmega.toFixed(2)}, α=${alpha.toFixed(2)}`);
    
    // Update physics ref for animation
    physicsRef.current = {
      theta: newTheta,
      omega: newOmega,
      alpha
    };
    
    // Update React state for UI (less frequently to avoid performance issues)
    setState({
      theta: newTheta,
      omega: newOmega,
      alpha
    });
  }, [params]); // Add params as dependency to ensure calculations use latest values

  // Render the pendulum to the canvas
  const renderPendulum = React.useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      console.warn("Canvas not available for rendering");
      return;
    }
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Get current physics state from ref
    const { theta, omega, alpha } = physicsRef.current;
    
    // Calculate pendulum position
    const pivotX = width / 2;
    const pivotY = height / 3;
    const pendulumLength = params.length * 100; // Increased scale factor for better visibility
    const bobX = pivotX + pendulumLength * Math.sin(theta);
    const bobY = pivotY + pendulumLength * Math.cos(theta);
    // Draw pivot
    ctx.beginPath();
    ctx.arc(pivotX, pivotY, 5, 0, 2 * Math.PI);
    ctx.fillStyle = '#555';
    ctx.fill();
    
    // Draw rod
    ctx.beginPath();
    ctx.moveTo(pivotX, pivotY);
    ctx.lineTo(bobX, bobY);
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw bob (mass)
    const bobRadius = Math.max(5, Math.sqrt(params.mass) * 5); // Size based on mass
    ctx.beginPath();
    ctx.arc(bobX, bobY, bobRadius, 0, 2 * Math.PI);
    ctx.fillStyle = '#c0392b';
    ctx.fill();
    
    // Draw info
    ctx.font = '12px Arial';
    ctx.fillStyle = '#000';
    ctx.fillText(`Angle: ${Math.round(theta * 180 / Math.PI)}°`, 10, 20);
    ctx.fillText(`Velocity: ${omega.toFixed(2)} rad/s`, 10, 40);
    ctx.fillText(`Acceleration: ${alpha.toFixed(2)} rad/s²`, 10, 60);
  }, [params]); // Add params as dependency to ensure renders with latest values

  // Setup and cleanup animation frame
  useEffect(() => {
    console.log("Setting up animation loop");
    // Reset previous time when parameters change
    previousTimeRef.current = 0;
    
    // Start animation loop
    requestRef.current = requestAnimationFrame(animate);
    
    // Cleanup function
    return () => {
      console.log("Cleaning up animation loop");
      cancelAnimationFrame(requestRef.current);
    };
  }, [animate, paused, params]); // Rerun when params, paused state, or animate function changes
  
  // Update physics parameters when they change
  useEffect(() => {
    console.log("Pendulum parameters changed:", params);
    // Reset physics when parameters change for immediate effect
    physicsRef.current = {
      theta: params.initialAngle,
      omega: 0,  // Reset velocity when parameters change for consistent behavior
      alpha: 0   // Reset acceleration
    };
    
    // Also update the state for UI updates
    setState({
      theta: params.initialAngle,
      omega: 0,
      alpha: 0
    });
    
    // Reset the animation timer when parameters change
    previousTimeRef.current = 0;
  }, [params]);

  return (
    <div className="pendulum-container">
      <canvas 
        ref={canvasRef} 
        width={400} 
        height={400} 
        className="pendulum-canvas"
        style={{
          border: '1px solid #ccc',
          background: '#f9f9f9',
          display: 'block',
          margin: '0 auto'
        }}
      />
      <div className="debug-info">
        <p>Length: {params.length}m, Mass: {params.mass}kg</p>
        <p>Gravity: {params.gravity}m/s², Damping: {params.damping}</p>
      </div>
    </div>
  );
};

export default Pendulum;

