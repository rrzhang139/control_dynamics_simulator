import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from controllers import basic_controller, energy_controller_acrobat
from integrators import rk4_step
from pydrake.all import LinearQuadraticRegulator

# Constants
dt = 0.0001  # Time step
T = 10     # Total simulation time
m1 = 1.0   # Mass of first link
m2 = 1.0   # Mass of second link
I1 = 1
I2 = 1
g = 9.8    # Gravity constant
L1 = 0.5    # Link length
L2 = 0.5    # Link length
b = 0.0    # Damping coefficient

# Control gains
k = 10.0

E_desired = m1*g*L1 + m2*g*L2
target_theta = np.pi

# Initial conditions
theta1 = np.pi + 0.05
theta2 = -0.1
omega1 = 0.0
omega2 = 0.0
alpha1 = 0.0
alpha2 = 0.0

# Control
u = 0
torque_limit = 1.0

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

def linearized_matrices():
    """ Computes the linearized A, B matrices for the Acrobot around the upright position. """
    
    # Mass-Inertia Matrix
    M11 = I1 + I2 + m2 * L1**2 + 2 * m2 * L1 * L2 * np.cos(theta2)
    M12 = I2 + m2 * L1 * L2 * np.cos(theta2)
    M21 = I2 + m2 * L1 * L2 * np.cos(theta2)
    M22 = I2
    M = np.array([[M11, M12], [M21, M22]])
    
    # Gravity Term (Linearized around upright)
    # Gravity gradient matrix (partial derivative of gravity torque with respect to q)
    # Linearized around the upright equilibrium point (theta1 = pi, theta2 = 0)
    dG_dq = np.array([
        [g * (m1 * L1 + m2 * L1 + m2 * L2), m2 * g * L2],
        [m2 * g * L2, m2 * g * L2]
    ])
    
    # Compute A matrix in block form: [0 I; M^-1 * dG_dq 0]
    # Note: B(q) is constant for Acrobot, so partial derivative terms drop out
    # Also, C terms drop out since velocity is zero at the equilibrium point
    A_top = np.block([np.zeros((2, 2)), np.eye(2)])
    A_bottom = np.block([np.linalg.inv(M) @ dG_dq, np.zeros((2, 2))])
    A = np.vstack((A_top, A_bottom))

    # Compute B matrix in block form: [0; M^-1 * B]
    # Where B = [0; 1] for Acrobot (actuation only at second joint)
    B = np.vstack((
        np.zeros((2, 1)),
        np.linalg.inv(M) @ np.array([[0], [1]])
    ))

    return A, B

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

def lqr(A, B, Q, R):
    """ Solves the Riccati equation and computes the LQR gain K. """
    print(A.shape, B.shape)
    S = scipy.linalg.solve_continuous_are(A, B, Q, R)
    K = np.linalg.inv(R) @ B.T @ S
    return K, S

# Define Cost Matrices
Q = np.diag([10, 10, 1, 1])  # Penalize state deviations
R = np.array([[1]])  # Penalize control effort
A, B = linearized_matrices()
print(A, B)
K, S = LinearQuadraticRegulator(A, B, Q, R) #lqr(A, B, Q, R)
print(K, S)

def update(frame):
    """ Update the animation for each frame """
    global theta1, theta2, omega1, omega2
    
    x = np.array([theta1, theta2, omega1, omega2])
    
    # WILL WORK
    u = -K @ x
    
    # WONT WORK. 
    # u = energy_controller_acrobat(m1, m2, L1, L2, omega1, omega2, g, theta1, theta2, E_desired, k)
    new_state = rk4_step(acrobot_dynamics, 0, x, u, dt)
    theta1, theta2, omega1, omega2 = new_state
    
    # Calculate positions
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    
    x2 = x1 + L2 * np.sin(theta1 + theta2)
    y2 = y1 - L2 * np.cos(theta1 + theta2)
    
    # Add error checking before setting data
    if np.isfinite(x1) and np.isfinite(y1) and np.isfinite(x2) and np.isfinite(y2):
        joint1.set_data([x1], [y1])
        joint2.set_data([x2], [y2])
        rod1.set_data([0, x1], [0, y1])
        rod2.set_data([x1, x2], [y1, y2])
    else:
        # If values are invalid, use empty sequences
        joint1.set_data([], [])
        joint2.set_data([], [])
        rod1.set_data([], [])
        rod2.set_data([], [])
    
    return joint1, joint2, rod1, rod2

# Create animation
ani = animation.FuncAnimation(fig, update, frames=int(T/dt), 
                              init_func=init, interval=dt*1000, blit=True)

plt.title("Acrobat (Double Pendulum) System")
plt.show()
