import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from controllers import energy_controller_pendulum
from integrators import euler_step

# Constants
dt = 0.01  # Time step (smaller for faster simulation)
T = 5      # Reduced simulation time
m = 1.0     # Mass
g = 9.8     # Gravity
L = 1.0     # Pendulum length
b = 0.1     # Damping coefficient

# Control Gains
Kp = 5.0  # Proportional gain for stabilization
Kd = 10.0   # Derivative gain for stabilization
k = 10.0   # Energy control gain

theta_target = np.pi  # Upright position
torque_limit = 1.0    # Maximum torque

# Desired energy for swing-up
E_desired = m * g * L

# Initial conditions
theta = np.pi / 16
angular_velocity = 0.0

# Setup animation
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Pendulum representation
bob, = plt.plot([], [], 'bo', markersize=14)  # Bob
rod, = plt.plot([], [], 'k-', lw=2)  # Rod

def init():
    """ Initialize animation """
    bob.set_data([], [])
    rod.set_data([], [])
    return rod, bob

def update(frame):
    """ Swing-up and stabilize pendulum """
    global theta, angular_velocity

    # Control Strategy: Use energy-based control for swing-up, then PD for stabilization
    if abs(theta - theta_target) > 0.2:  # Swing-up mode (far from upright)
        u = energy_controller_pendulum(m, L, angular_velocity, g, theta, E_desired, k)  # Energy injection control
    else:  # Stabilization mode (near upright)
        u = m*g*L*np.sin(theta) - Kp * (theta - theta_target) - Kd * angular_velocity  # PD control
    
    # Apply torque limits
    u = np.clip(u, -torque_limit, torque_limit)

    # Define pendulum dynamics function for the integrator
    def pendulum_dynamics(t, state, u):
        theta, omega = state
        angular_acceleration = (u - b * omega - m * g * L * np.sin(theta)) / (m * L**2)
        return [omega, angular_acceleration]
    
    # Use euler_step from integrators module
    state = np.array([theta, angular_velocity])
    new_state = euler_step(pendulum_dynamics, 0, state, u, dt)
    theta, angular_velocity = new_state

    # Compute new bob position
    x = L * np.sin(theta)
    y = -L * np.cos(theta)

    # Update visualization
    bob.set_data(x, y)
    rod.set_data([0, x], [0, y])

    return rod, bob

# Create animation
ani = animation.FuncAnimation(fig, update, frames=int(T/dt), init_func=init, interval=dt*1000, blit=True)

plt.title("Energy-Based Swing-Up + PD Stabilization")
plt.show()
