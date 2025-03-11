import React, { useRef, useEffect, useState, useCallback } from 'react';

// This component handles physics simulation and rendering of a controlled pendulum
const PendulumControl = ({ params, paused }) => {
  const canvasRef = useRef(null);
  const requestRef = useRef(null);
  const previousTimeRef = useRef(0);
  
  // Use refs to track physics values for animation
  const physicsRef = useRef({
    theta: params.initialAngle,     // Current angle (radians)
    omega: 0,                       // Angular velocity
    alpha: 0,                       // Angular acceleration
    torque: 0                       // Control torque
  });
  
  // State for UI updates (not used directly in animation calculations)
  const [state, setState] = useState({
    theta: params.initialAngle,     
    omega: 0,                       
    alpha: 0,
    torque: 0
  });
  
  // Animation/simulation loop
  const animate = useCallback((time) => {
    if (previousTimeRef.current === 0) {
      previousTimeRef.current = time;
    }
    
    const deltaTime = (time - previousTimeRef.current) / 1000; // Convert to seconds
    previousTimeRef.current = time;
    
    if (!paused) {
      updatePhysics(deltaTime);
    }
    
    renderPendulum();
    requestRef.current = requestAnimationFrame(animate);
  }, [paused, params]);

  // Calculate control torque
  const calculateControlTorque = useCallback((theta, omega) => {
    const { 
      mass, 
      length, 
      gravity, 
      kp, 
      kd, 
      energyGain, 
      targetAngle,
      torqueLimit 
    } = params;
    
    // Compute total energy (kinetic + potential)
    const E = 0.5 * mass * length**2 * omega**2 - mass * gravity * length * Math.cos(theta);
    
    // Desired energy at upright position
    const E_desired = mass * gravity * length;
    
    // Energy difference
    const E_tilde = E - E_desired;
    
    let torque;
    
    // Control Strategy: Use energy-based control for swing-up, then PD for stabilization
    if (Math.abs(theta - targetAngle) > 0.2) {  // Swing-up mode (far from upright)
      torque = -energyGain * omega * E_tilde;  // Energy injection control
    } else {  // Stabilization mode (near upright)
      torque = -kp * (theta - targetAngle) - kd * omega;  // PD control
    }
    
    // Apply torque limits
    return Math.max(-torqueLimit, Math.min(torqueLimit, torque));
  }, [params]);

  // Update physics using double integration with control
  const updatePhysics = useCallback((dt) => {
    // Don't update if dt is too large (e.g., if tab was inactive)
    if (dt > 0.1) {
      return;
    }
    
    // Get parameters
    const g = params.gravity;
    const L = params.length;
    const m = params.mass;
    const b = params.damping;
    
    // Get current state from ref
    const { theta, omega } = physicsRef.current;
    
    // Calculate control torque
    const torque = calculateControlTorque(theta, omega);
    
    // Calculate angular acceleration (α) with control torque
    const alpha = (torque - b * omega - m * g * L * Math.sin(theta)) / (m * L**2);
    
    // First integration: velocity = previous velocity + acceleration * dt
    const newOmega = omega + alpha * dt;
    
    // Second integration: position = previous position + velocity * dt
    const newTheta = theta + newOmega * dt;
    
    // Update physics ref for animation
    physicsRef.current = {
      theta: newTheta,
      omega: newOmega,
      alpha,
      torque
    };
    
    // Update React state for UI (less frequently to avoid performance issues)
    setState({
      theta: newTheta,
      omega: newOmega,
      alpha,
      torque
    });
  }, [params, calculateControlTorque]);

  // Render the pendulum to the canvas
  const renderPendulum = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Get current physics state from ref
    const { theta, omega, alpha, torque } = physicsRef.current;
    
    // Calculate pendulum position
    const pivotX = width / 2;
    const pivotY = height / 3;
    const pendulumLength = params.length * 100; // Scale for better visibility
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
    
    // Color based on control mode (swing-up vs stabilization)
    if (Math.abs(theta - params.targetAngle) > 0.2) {
      ctx.fillStyle = '#3498db'; // Blue for swing-up
    } else {
      ctx.fillStyle = '#2ecc71'; // Green for stabilization
    }
    ctx.fill();
    
    // Draw a line to represent torque
    if (torque !== 0) {
      const torqueScale = 20 * (torque / params.torqueLimit);
      ctx.beginPath();
      ctx.moveTo(bobX, bobY);
      ctx.lineTo(bobX + torqueScale, bobY);
      ctx.strokeStyle = torque > 0 ? '#e74c3c' : '#8e44ad'; // Red or purple
      ctx.lineWidth = 2;
      ctx.stroke();
    }
    
    // Draw target position (inverted pendulum)
    const targetX = pivotX + pendulumLength * Math.sin(params.targetAngle);
    const targetY = pivotY + pendulumLength * Math.cos(params.targetAngle);
    ctx.beginPath();
    ctx.arc(targetX, targetY, 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgba(39, 174, 96, 0.3)';
    ctx.fill();
    
    // Draw dashed line to target
    ctx.beginPath();
    ctx.setLineDash([5, 5]);
    ctx.moveTo(pivotX, pivotY);
    ctx.lineTo(targetX, targetY);
    ctx.strokeStyle = 'rgba(39, 174, 96, 0.5)';
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Draw info
    ctx.font = '12px Arial';
    ctx.fillStyle = '#000';
    ctx.fillText(`Angle: ${Math.round(theta * 180 / Math.PI)}°`, 10, 20);
    ctx.fillText(`Velocity: ${omega.toFixed(2)} rad/s`, 10, 40);
    ctx.fillText(`Control: ${torque.toFixed(2)} Nm`, 10, 60);
    
    // Draw control mode
    ctx.font = '14px Arial';
    if (Math.abs(theta - params.targetAngle) > 0.2) {
      ctx.fillText('Mode: Energy-based Swing-up', 10, height - 20);
    } else {
      ctx.fillText('Mode: PD Stabilization', 10, height - 20);
    }
  }, [params]);

  // Setup and cleanup animation frame
  useEffect(() => {
    previousTimeRef.current = 0;
    requestRef.current = requestAnimationFrame(animate);
    
    return () => {
      cancelAnimationFrame(requestRef.current);
    };
  }, [animate, paused, params]);
  
  // Update physics parameters when they change
  useEffect(() => {
    physicsRef.current = {
      theta: params.initialAngle,
      omega: 0,
      alpha: 0,
      torque: 0
    };
    
    setState({
      theta: params.initialAngle,
      omega: 0,
      alpha: 0,
      torque: 0
    });
    
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
        <p>Control Gains: Kp={params.kp}, Kd={params.kd}, Energy={params.energyGain}</p>
        <p>Target Angle: {Math.round(params.targetAngle * 180 / Math.PI)}°</p>
      </div>
    </div>
  );
};

export default PendulumControl;

