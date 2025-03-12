import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from controllers import acrobot_linearized_matrices, lqr_solve, acrobot_lqr_controller

###############################################################################
#                        PARAMETERS AND CONSTANTS                             #
###############################################################################
# Simulation parameters
dt = 0.01     # Time step
T  = 10.0     # Total simulation time

# Physical parameters for the Acrobot
m1 = 1.0      # Mass of link 1
m2 = 1.0      # Mass of link 2
I1 = 1.0      # Moment of inertia for link 1
I2 = 1.0      # Moment of inertia for link 2
L1 = 0.5      # Length of link 1
L2 = 0.5      # Length of link 2
g  = 9.8      # Gravity

# Torque limit at the second joint
torque_limit = 1.0

# Initial conditions (slightly perturbed from the upright equilibrium)
# The equilibrium of interest is: theta1 = pi, theta2 = 0, angular velocities = 0
theta1_0  = np.pi + 0.01
theta2_0  = -0.0
omega1_0  = 0.0
omega2_0  = 0.0

###############################################################################
#                      DYNAMICS FUNCTION                                      #
###############################################################################
def acrobot_dynamics(t, state, u):
    """
    Compute the full nonlinear dynamics of the Acrobot (manipulator form).
    
    state = [theta1, theta2, omega1, omega2]
    u     = scalar torque (applied at the second joint)
    """
    theta1, theta2, omega1, omega2 = state
    
    # Mass-Inertia Matrix M(q)
    M11 = I1 + I2 + m2*L1**2 + 2*m2*L1*L2*np.cos(theta2)
    M12 = I2 + m2*L1*L2*np.cos(theta2)
    M21 = I2 + m2*L1*L2*np.cos(theta2)
    M22 = I2
    M = np.array([[M11, M12],
                  [M21, M22]])
    
    # Coriolis/centrifugal terms C(q, qdot)*qdot
    # For the Acrobot:
    #   C1 = -m2 * L1 * L2 * sin(theta2) * (2*omega1*omega2 + omega2^2)
    #   C2 =  m2 * L1 * L2 * sin(theta2) * omega1^2
    C1 = -m2*L1*L2*np.sin(theta2)* (2*omega1*omega2 + omega2**2)
    C2 =  m2*L1*L2*np.sin(theta2)* (omega1**2)
    Cvec = np.array([C1, C2])
    
    # Gravity terms tau_g(q)
    #   G1 = (m1+m2)*g*L1*sin(theta1) + m2*g*L2*sin(theta1 + theta2)
    #   G2 = m2*g*L2*sin(theta1 + theta2)
    G1 = (m1 + m2)*g*L1*np.sin(theta1) + m2*g*L2*np.sin(theta1 + theta2)
    G2 = m2*g*L2*np.sin(theta1 + theta2)
    Gvec = np.array([G1, G2])
    
    # Control input is applied only at joint 2
    # B = [0; 1], so the torque vector is [0, u]^T
    # Clip to torque limits
    u_clamped = np.clip(u, -torque_limit, torque_limit)
    Bvec = np.array([0.0, 1.0]) * u_clamped
    
    # Solve for angular accelerations = M^{-1} (B*u - C - G)
    accels = np.linalg.solve(M, Bvec - Cvec - Gvec)
    
    # Return the state derivatives
    return np.array([omega1, omega2, accels[0], accels[1]])

###############################################################################
#                          SETUP LQR CONTROLLER                               #
###############################################################################
# Get linearization around the upright equilibrium
A_lin, B_lin = acrobot_linearized_matrices(m1, m2, I1, I2, L1, L2, g)

# Define cost matrices: you can tune these to emphasize different states
Q = np.diag([10.0, 10.0, 1.0, 1.0]) 
R = np.array([[1.0]])

# Compute LQR gains
K_lqr, S_lqr = lqr_solve(A_lin, B_lin, Q, R)

print("Linearized A:\n", A_lin)
print("Linearized B:\n", B_lin)
print("LQR Gain K:\n", K_lqr)


###############################################################################
#                           SIMULATION / ANIMATION                            #
###############################################################################
# Prepare for simulation
num_steps = int(T / dt)
state = np.array([theta1_0, theta2_0, omega1_0, omega2_0])
reference_state = np.array([np.pi, 0.0, 0.0, 0.0])  # Upright equilibrium

# Set up figure for animation
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.set_title("Acrobot Balancing with LQR")

# Plot elements
joint1, = ax.plot([], [], 'bo', markersize=8)   # First joint
joint2, = ax.plot([], [], 'ro', markersize=8)   # Second joint
rod1,   = ax.plot([], [], 'k-', lw=2)
rod2,   = ax.plot([], [], 'k-', lw=2)

def init_anim():
    joint1.set_data([], [])
    joint2.set_data([], [])
    rod1.set_data([], [])
    rod2.set_data([], [])
    return joint1, joint2, rod1, rod2

def update_anim(frame):
    """
    Single time-step update for the animation.
    Applies the LQR torque and integrates one step.
    """
    global state
    
    # Apply LQR control using our controller module
    u = acrobot_lqr_controller(state, reference_state, K_lqr)
    
    # Integrate one step
    xdot = acrobot_dynamics(0, state, u)
    state = state + xdot*dt

    # Unpack new state
    theta1, theta2, _, _ = state

    # Get link endpoints for plotting
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta1 + theta2)
    y2 = y1 - L2 * np.cos(theta1 + theta2)
    
    # Update lines and joints
    joint1.set_data([x1], [y1])
    joint2.set_data([x2], [y2])
    rod1.set_data([0, x1], [0, y1])
    rod2.set_data([x1, x2], [y1, y2])
    
    return joint1, joint2, rod1, rod2

ani = animation.FuncAnimation(
    fig, update_anim, frames=num_steps,
    init_func=init_anim, blit=True, interval=dt*1000
)
plt.show()
