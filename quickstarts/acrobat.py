import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from controllers import basic_controller, energy_controller_acrobat

# Constants
dt = 0.05  # Time step
T = 10     # Total simulation time
m1 = 1.0   # Mass of first link
m2 = 1.0   # Mass of second link
I1 = 1
I2 = 1
g = 9.8    # Gravity constant
L1 = 0.5    # Link length
L2 = 0.5    # Link length
b = 0.5    # Damping coefficient

# Control gains
k = 1.0

E_desired = m1*g*L1 + m2*g*L2
target_theta = np.pi

# Initial conditions
theta1 = np.pi / 16
theta2 = 0.0
omega1 = 0.0
omega2 = 0.0
alpha1 = 0.0
alpha2 = 0.0

# Control
u = 0
torque_limit = 5.0

# Setup animation
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Acrobat representation
joint1, = plt.plot([], [], 'bo', markersize=10)  # First joint
joint2, = plt.plot([], [], 'ro', markersize=10)  # Second joint
rod1, = plt.plot([], [], 'k-', lw=2)  # First rod
rod2, = plt.plot([], [], 'k-', lw=2)  # Second rod

def init():
    """ Initialize animation """
    joint1.set_data([], [])
    joint2.set_data([], [])
    rod1.set_data([], [])
    rod2.set_data([], [])
    return joint1, joint2, rod1, rod2

def rk4_step(func, t, state, u, dt):
    """ Implements one step of RK4 integration. """
    k1 = np.array(func(t, state, u)) * dt
    k2 = np.array(func(t + dt/2, state + k1/2, u)) * dt
    k3 = np.array(func(t + dt/2, state + k2/2, u)) * dt
    k4 = np.array(func(t + dt, state + k3, u)) * dt
    return state + (k1 + 2*k2 + 2*k3 + k4) / 6

def acrobot_dynamics(t, state, u):
    """ Computes the equations of motion for the Acrobot. """
    theta1, theta2, ang_vel1, ang_vel2 = state

    # Mass-Inertia Matrix
    M11 = I1 + I2 + m2 * L1**2 + 2 * m2 * L1 * L2 * np.cos(theta2)
    M12 = I2 + m2 * L1 * L2 * np.cos(theta2)
    M21 = I2 + m2 * L1 * L2 * np.cos(theta2)
    M22 = I2
    M = np.array([[M11, M12], [M21, M22]])

    # Coriolis & Centrifugal Forces
    C1 = -m2 * L1 * L2 * np.sin(theta2) * ang_vel2 * (2 * ang_vel1 + ang_vel2)
    C2 = m2 * L1 * L2 * np.sin(theta2) * ang_vel1**2
    C = np.array([C1, C2])

    # Gravity Terms
    G1 = (m1 + m2) * g * L1 * np.sin(theta1) + m2 * g * L2 * np.sin(theta1 + theta2)
    G2 = m2 * g * L2 * np.sin(theta1 + theta2)
    G = np.array([G1, G2])

    # Control Input (Actuator only at joint 2)
    B = np.array([0, 1])
    u = np.clip(u, -torque_limit, torque_limit)  # Apply torque limits

    # Solve for angular accelerations
    accels = np.linalg.solve(M, B * u - C - G)
    
    return [ang_vel1, ang_vel2, accels[0], accels[1]]

def update(frame):
    """ Update the animation for each frame """
    global theta1, theta2, omega1, omega2
    
    # WONT WORK. 
    u = energy_controller_acrobat(m1, m2, L1, L2, omega1, omega2, g, theta1, theta2, E_desired, k)
    
    state = np.array([theta1, theta2, omega1, omega2])
    new_state = rk4_step(acrobot_dynamics, 0, state, u, dt)
    
    theta1, theta2, omega1, omega2 = new_state
    
    # Calculate positions
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    
    x2 = x1 + L2 * np.sin(theta1 + theta2)
    y2 = y1 - L2 * np.cos(theta1 + theta2)
    
    # Update visualization
    joint1.set_data(x1, y1)
    joint2.set_data(x2, y2)
    rod1.set_data([0, x1], [0, y1])
    rod2.set_data([x1, x2], [y1, y2])
    
    return joint1, joint2, rod1, rod2

# Create animation
ani = animation.FuncAnimation(fig, update, frames=int(T/dt), 
                              init_func=init, interval=dt*1000, blit=True)

plt.title("Acrobat (Double Pendulum) System")
plt.show()
