import React, { useEffect, useRef } from 'react';

const PendulumControl = ({ params, paused }) => {
  // Reference to the canvas element
  const canvasRef = useRef(null);
  
  // Animation frame and simulation state references
  const requestRef = useRef();
  const previousTimeRef = useRef();
  const stateRef = useRef({
    theta: params.initialAngle,
    angular_velocity: 0,
    angular_acceleration: 0
  });
  
  // Compute desired energy
  const E_desired = params.mass * params.gravity * params.length;
  
  // Effect for handling the animation loop
  useEffect(() => {
    // Initialize canvas
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Canvas dimensions
    const width = canvas.width;
    const height = canvas.height;
    
    // Set origin to center of canvas
    const centerX = width / 2;
    const centerY = height / 3;
    
    // Scale factor for visualization (pixels per meter)
    const pendulumLength = params.length * 100; // Increased scale factor for better visibility
    
    // Animation loop
    const animate = (time) => {
      if (previousTimeRef.current === undefined) {
        previousTimeRef.current = time;
        requestRef.current = requestAnimationFrame(animate);
        return;
      }
      
      // Calculate time delta in seconds
      const deltaTime = (time - previousTimeRef.current) / 1000;
      previousTimeRef.current = time;
      
      // If not paused, update the simulation
      if (!paused) {
        // Access current state
        let { theta, angular_velocity, angular_acceleration } = stateRef.current;
        
        // Multiple simulation steps per frame for accuracy
        const numSteps = 5;
        const dt = deltaTime / numSteps;
        
        for (let i = 0; i < numSteps; i++) {
          // Calculate system energy
          const E = 0.5 * params.mass * params.length**2 * angular_velocity**2 - 
                   params.mass * params.gravity * params.length * Math.cos(theta);
          const E_tilde = E - E_desired;
          
          // Control strategy
          let u;
          if (Math.abs(theta - params.targetAngle) > 0.2) {
            // Swing-up mode: energy control
            u = -params.energyGain * angular_velocity * E_tilde;
          } else {
            // Stabilization mode: PD control
            u = params.mass*params.gravity*params.length*Math.sin(theta) - params.kp * (theta - params.targetAngle) - params.kd * angular_velocity;
          }
          
          // Apply torque limits
          u = Math.max(-params.torqueLimit, Math.min(u, params.torqueLimit));
          
          // Compute acceleration
          const angular_acceleration = (u - params.damping * angular_velocity - 
                                     params.mass * params.gravity * params.length * Math.sin(theta)) / 
                                     (params.mass * params.length**2);
          
          // Euler integration
          angular_velocity += angular_acceleration * dt;
          theta += angular_velocity * dt;
          
          // Normalize theta to be between -π and π
          theta = (theta + Math.PI) % (2 * Math.PI) - Math.PI;
        }
        
        // Update state reference
        stateRef.current = { theta, angular_velocity, angular_acceleration };
      }
      
      // Clear canvas
      ctx.clearRect(0, 0, width, height);
      
      // Draw pivot
      ctx.beginPath();
      ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI);
      ctx.fillStyle = '#555';
      ctx.fill();
      
      // Calculate pendulum position
      const { theta, angular_velocity, angular_acceleration } = stateRef.current;
      const x = centerX + pendulumLength * Math.sin(theta);
      const y = centerY + pendulumLength * Math.cos(theta);
      
      // Draw rod
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Draw bob (mass)
      const bobRadius = Math.max(5, Math.sqrt(params.mass) * 5); // Size based on mass
      ctx.beginPath();
      ctx.arc(x, y, bobRadius, 0, 2 * Math.PI);
      ctx.fillStyle = '#c0392b';
      ctx.fill();

      ctx.font = '12px Arial';
      ctx.fillStyle = '#000';
      ctx.fillText(`Angle: ${Math.round(theta * 180 / Math.PI)}°`, 10, 20);
      ctx.fillText(`Velocity: ${angular_velocity.toFixed(2)} rad/s`, 10, 40);
      ctx.fillText(`Acceleration: ${angular_acceleration.toFixed(2)} rad/s²`, 10, 60);
      
      // Draw target angle indicator
      const targetX = centerX + pendulumLength * Math.sin(params.targetAngle) * 0.8;
      const targetY = centerY + pendulumLength * Math.cos(params.targetAngle) * 0.8;
      ctx.beginPath();
      ctx.arc(targetX, targetY, 5, 0, 2 * Math.PI);
      ctx.fillStyle = 'green';
      ctx.fill();
      
      // Continue animation loop
      requestRef.current = requestAnimationFrame(animate);
    };
    
    // Start animation
    requestRef.current = requestAnimationFrame(animate);
    
    // Cleanup on unmount
    return () => {
      cancelAnimationFrame(requestRef.current);
    };
  }, [params, paused]);
  
  // Reset simulation when params change
  useEffect(() => {
    stateRef.current = {
      theta: params.initialAngle,
      angular_velocity: 0,
      angular_acceleration: 0
    };
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

export default PendulumControl;
