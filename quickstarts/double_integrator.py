import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
dt = 0.01  # Time step
T = 10      # Total simulation time
time_steps = int(T / dt)

# Initial conditions
q = -10      # Initial position
q_dot = 1   # Initial velocity
u_max = 1   # Maximum control input (acceleration)


# Set up figure for animation
fig, ax = plt.subplots()
ax.set_xlim(-15, 15)  # Wider range to see the full motion
ax.set_ylim(-5, 5)    # Adjusted for visualization
ax.set_aspect('equal')
ax.set_title("Bang-Bang Double Integrator using Differential Equations")

# Plot elements
block, = ax.plot([], [], 'bo', markersize=8)

def init_anim():
    """ Initialize animation frame. """
    block.set_data([], [])
    return block,

def update_anim(frame):
    """ Update function for animation. """
    global q, q_dot
    
    # Compute bang-bang control
    if q_dot**2 / (2 * u_max) > abs(q):  # Braking condition
        u = -np.sign(q_dot) * u_max  # Brake to stop at the origin
    else:  # Accelerate toward the origin
        u = -np.sign(q) * u_max
    
    # First integrate velocity (Euler step)
    q_dot += u * dt
    
    # Then integrate position (Euler step using updated velocity)
    q += q_dot * dt
    
    # Update block position
    block.set_data([q], [0])
    
    return block,

# Create animation
ani = animation.FuncAnimation(
    fig, update_anim, frames=time_steps,
    init_func=init_anim, blit=True, interval=dt*1000
)

plt.show()
