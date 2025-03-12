import numpy as np
import scipy.linalg

def basic_controller(theta, omega, target_theta, Kd: float = 5.0, Kp: float = 10.0):
    return -Kd * (theta - target_theta) - Kp * omega

def energy_controller_pendulum(m, L, omega, g, theta, E_desired, k):
    # Compute total energy
    E = 0.5 * m * L**2 * omega**2 - m * g * L * np.cos(theta)
    E_tilde = E - E_desired  # Energy difference
    return -k * omega * E_tilde  # Energy injection control

def energy_controller_acrobat(m1, m2, L1, L2, omega1, omega2, g, theta1, theta2, E_desired, gains):
    # Controller gains
    k1, k2, k3 = gains

    # Inertia matrix (M)
    M11 = (m1 + m2) * L1**2 + m2 * L2**2 + 2 * m2 * L1 * L2 * np.cos(theta2)
    M22 = m2 * L2**2
    M12 = M21 = m2 * L2**2 + m2 * L1 * L2 * np.cos(theta2)
    M = np.array([[M11, M12], [M21, M22]])

    # Potential Energy (U)
    U = -(m1 + m2) * g * L1 * np.cos(theta1) - m2 * g * L2 * np.cos(theta1 + theta2)

    # Kinetic Energy (K)
    omega = np.array([omega1, omega2])
    K = 0.5 * omega.T @ M @ omega

    # Total energy
    E = K + U

    # Energy difference
    E_tilde = E - E_desired

    # Intermediate control input
    u_bar = omega1 * E_tilde

    # Desired acceleration (collocated partial feedback linearization)
    ddq2_desired = -k1 * theta2 - k2 * omega2 + k3 * u_bar

    return ddq2_desired

def lqr_solve(A, B, Q, R):
    """
    Solve the continuous-time LQR problem for x' = A x + B u.
    
    Parameters:
        A: System matrix of shape (n, n)
        B: Control matrix of shape (n, m)
        Q: State cost matrix of shape (n, n)
        R: Control cost matrix of shape (m, m)
        
    Returns:
        K: LQR gain matrix of shape (m, n)
        S: Solution to the continuous-time algebraic Riccati equation
    """
    S = scipy.linalg.solve_continuous_are(A, B, Q, R)
    K = np.linalg.inv(R) @ B.T @ S
    return K, S

def lqr_controller(state, reference_state, K):
    """
    Apply LQR control to track a reference state.
    
    Parameters:
        state: Current state vector
        reference_state: Desired state vector
        K: LQR gain matrix
        
    Returns:
        u: Control input
    """
    state_error = state - reference_state
    u = -K @ state_error
    return u

def acrobot_linearized_matrices(m1, m2, I1, I2, L1, L2, g):
    """
    Linearize the Acrobot dynamics around the upright equilibrium:
    theta1 = pi, theta2 = 0, omega1 = 0, omega2 = 0, u = 0.
    
    Parameters:
        m1: Mass of link 1
        m2: Mass of link 2
        I1: Moment of inertia for link 1
        I2: Moment of inertia for link 2
        L1: Length of link 1
        L2: Length of link 2
        g: Gravity constant
        
    Returns:
        A: System matrix (4x4) for the continuous-time linearized dynamics
        B: Control matrix (4x1) for the continuous-time linearized dynamics
    """
    # Evaluate M at the equilibrium (theta2 = 0)
    M11 = I1 + I2 + m2*L1**2 + 2*m2*L1*L2  # cos(0)=1
    M12 = I2 + m2*L1*L2
    M21 = I2 + m2*L1*L2
    M22 = I2
    M_eq = np.array([[M11, M12],
                     [M21, M22]])
    
    # Derivative of gravity terms w.r.t. [theta1, theta2], at (theta1=pi, theta2=0)
    dG_dq = np.array([
        [g*(m1*L1 + m2*L1 + m2*L2), m2*g*L2],
        [m2*g*L2, m2*g*L2]
    ])
    
    # The linearized A matrix in block form
    zero_2x2 = np.zeros((2, 2))
    eye_2x2 = np.eye(2)
    Minv = np.linalg.inv(M_eq)
    
    A_top = np.hstack([zero_2x2, eye_2x2])
    A_bottom = np.hstack([Minv @ dG_dq, zero_2x2])
    A = np.vstack([A_top, A_bottom])
    
    # The linearized B matrix in block form
    B_bottom = Minv @ np.array([[0.0], [1.0]])
    B_top = np.zeros((2, 1))
    B = np.vstack([B_top, B_bottom])
    
    return A, B

def acrobot_lqr_controller(state, reference_state, K):
    """
    Apply LQR control for an acrobot about the upright equilibrium.
    
    Parameters:
        state: Current state [theta1, theta2, omega1, omega2]
        reference_state: Reference state [theta1_ref, theta2_ref, omega1_ref, omega2_ref]
        K: LQR gain matrix
        
    Returns:
        u: Control torque
    """
    # For the upright equilibrium controller, we need to shift theta1 by pi
    # because the linearization is around [pi, 0, 0, 0]
    state_shifted = state.copy()
    state_shifted[0] -= np.pi
    
    reference_shifted = reference_state.copy()
    reference_shifted[0] -= np.pi
    
    return lqr_controller(state_shifted, reference_shifted, K)

def pendulum_linearized_matrices(m, L, g):
    """
    Linearize the pendulum dynamics around the upright equilibrium:
    theta = pi, omega = 0, u = 0.
    
    Parameters:
        m: Mass of the pendulum
        L: Length of the pendulum
        g: Gravity constant
        
    Returns:
        A: System matrix (2x2) for the continuous-time linearized dynamics
        B: Control matrix (2x1) for the continuous-time linearized dynamics
    """
    # For a simple pendulum, the linearized matrices around the upright position
    J = m * L**2  # Moment of inertia
    
    A = np.array([
        [0, 1],
        [g/L, 0]
    ])
    
    B = np.array([
        [0],
        [1/J]
    ])
    
    return A, B

def design_lqr_controller(A, B, Q, R):
    """
    Design an LQR controller for a linear system.
    
    Parameters:
        A: System matrix
        B: Control matrix
        Q: State cost matrix
        R: Control cost matrix
        
    Returns:
        K: LQR gain matrix
    """
    K, _ = lqr_solve(A, B, Q, R)
    return K
