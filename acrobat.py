import numpy as np
import matplotlib.pyplot as plt

# Constants
dt = 0.1  # Time step
T = 100     # Total simulation time
steps = int(T / dt)  # Number of iterations
m1 = 1.0    # Mass
m2 = 1.0
g = 9.8    # Gravity constant
L = 0.5    # Pendulum length
b = 0.5    # Damping coefficient

# States
# [q, \dot q]
theta1 = 0
theta2 = 0
ang_vel1 = 0.0    # Initial angular velocity
ang_vel2 = 0.0

# Control
u = 0

# Storage for results
angles = []
times = np.arange(0, T, dt)

# Setup animation before simulation
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Pendulum representation
joint1, = plt.plot([], [], 'bo', markersize=14)
joint2, = plt.plot([], [], 'bo', markersize=14)
rod1, = plt.plot([], [], 'k-', lw=2)
rod2, = plt.plot([], [], 'k-', lw=2)

# Function to update the animation during debugging
def update_animation(theta1: float, theta2: float):
    # ASCII visualization of acrobat (double pendulum) coordinates:
    #
    #    pivot (0,0)
    #       o
    #       |\
    #       | \  rod1 (length L)
    #       |  \
    #       |   \
    #       |    \
    #       |     \
    #       |      o------ middle joint (x1,y1)
    #       |      |\
    #       |      | \  rod2 (length L)
    #       |      |  \
    #       |      |   \
    #       |      |    \
    #       |      |     o  end effector (x2,y2)
    #  -----+------+--------- x-axis
    #       |      |
    #       |      |
    #       v      |
    #     y-axis   |
    #              |
    #
    # First pendulum:
    # x1 = L * sin(θ1)
    # y1 = -L * cos(θ1)
    #
    # Second pendulum (relative to first joint):
    # x2 = x1 + L * sin(θ2)
    # y2 = y1 - L * cos(θ2)
    #
    # For θ = 0: straight down
    # For θ = π/2: horizontal right
    # For θ = π: straight up
    # For θ = 3π/2: horizontal left
    x1 = L * np.sin(theta1)
    y1 = -L * np.cos(theta1)
    joint1.set_data(x1, y1)
    rod1.set_data([0, x1], [0, y1])
    
    x2 = x1 + L * np.sin(theta2)
    y2 = y1 - L * np.cos(theta2)
    joint2.set_data(x2, y2)
    rod2.set_data([x1, x2], [y1, y2])
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)  # Small pause to allow animation to update

# Show initial state
plt.ion()  # Turn on interactive mode
plt.title("Pendulum System Animation")
update_animation(theta1, theta2)  # We initialize the plots with initial position, bob etc

# Euler Integration with animation updates
# For a double pendulum, we need to solve the coupled differential equations
# The equations of motion for a double pendulum are complex and involve:
# - Calculating forces and torques at both joints
# - Accounting for the interaction between the two pendulums
# - Handling the nonlinear dynamics

# We could use Euler integration as follows:
# 1. Calculate angular accelerations for both pendulums using the full equations
# 2. Update angular velocities using these accelerations
# 3. Update angles using the updated velocities

# However, Euler integration may be unstable for this system
# Better alternatives would be:
# - Runge-Kutta methods (RK4)
# - Velocity Verlet integration
# - Symplectic integrators that preserve energy better

# For now, we'll need to implement the proper equations of motion
# for the double pendulum system with appropriate integration
for t in times:
    # TODO: Implement proper double pendulum equations and integration
    # M * \dotdot theta + C * \dot theta + G = Bu
    
    pass

    update_animation(theta)
    angles.append(theta)    

# Keep the plot open when done
plt.ioff()  # Turn off interactive mode
plt.show(block=True)

