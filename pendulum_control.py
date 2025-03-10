import numpy as np
import matplotlib.pyplot as plt

# Constants
dt = 0.1  # Time step
T = 100     # Total simulation time
steps = int(T / dt)  # Number of iterations
m = 1.0    # Mass

# States
theta = 0
angular_velocity = 0.0    # Initial angular velocity
angular_acceleration = 0.0
g = 9.8    # Gravity constant
L = 1.0    # Pendulum length
b = 0.0    # Damping coefficient

# Control
Kp = 5.0   # Proportional gain (stiffness)
Kd = 5.0    # Derivative gain (damping)
theta_target = np.pi  # Target upright position
torque_limit = 5.0   # Maximum torque that can be applied (N·m)

# Storage for results
angles = []
times = np.arange(0, T, dt)

# Setup animation before simulation
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Pendulum representation
bob, = plt.plot([], [], 'bo', markersize=14)  # Blue ball for bob
rod, = plt.plot([], [], 'k-', lw=2)  # Rod line

# Function to update the animation during debugging
def update_animation(theta: float):
    # ASCII visualization of pendulum coordinates:
    #
    #    pivot (0,0)
    #       o
    #       |\ 
    #       | \  rod (length L)
    #       |  \
    #       |   \
    #       |    \
    #       |     \
    #       |      \
    #  -----+-------o------ x-axis
    #       |      bob (x,y)
    #       |
    #       |
    #       v
    #     y-axis
    #
    # x = L * sin(θ)
    # y = -L * cos(θ)
    #
    # For θ = 0: bob at (0,-L) (straight down)
    # For θ = π/2: bob at (L,0) (horizontal right)
    # For θ = π: bob at (0,L) (straight up)
    # For θ = 3π/2: bob at (-L,0) (horizontal left)
    x = L * np.sin(theta)
    y = -L * np.cos(theta)
    bob.set_data(x, y)
    rod.set_data([0, x], [0, y])
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)  # Small pause to allow animation to update

# Show initial state
plt.ion()  # Turn on interactive mode
plt.title("Pendulum System Animation")
update_animation(theta)  # We initialize the plots with initial position, bob etc

# Euler Integration with animation updates
for t in times:
    # breakpoint()
    
    # Inverting gravity, also need PD controller to stabilize it.
    E = 0.5 * m*L**2*angular_velocity**2 - m*g*L
    E_tilde = E - m*g*L
    u = -Kd*angular_velocity*E_tilde #- b*angular_velocity + m*g*L*np.sin(theta) # - Kd*angular_velocity - Kp*(theta - np.pi)
    
    # Apply torque limits
    # u = np.clip(u, -torque_limit, torque_limit)
    
    angular_acceleration = (u - b*angular_velocity - (m*g*L) * np.sin(theta)) / (m*L**2)
    angular_velocity = angular_velocity + angular_acceleration * dt
    theta = theta + angular_velocity * dt

    update_animation(theta)
    angles.append(theta)    

# Keep the plot open when done
plt.ioff()  # Turn off interactive mode
plt.show(block=True)
