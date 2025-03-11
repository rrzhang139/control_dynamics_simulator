import numpy as np

def basic_controller(theta, omega, target_theta, Kd: float = 5.0, Kp: float = 10.0):
    return -Kd * (theta - target_theta) - Kp * omega

def energy_controller_pendulum(m, L, omega, g, theta, E_desired, k):
    # Compute total energy
    E = 0.5 * m * L**2 * omega**2 - m * g * L * np.cos(theta)
    E_tilde = E - E_desired  # Energy difference
    return -k * omega * E_tilde  # Energy injection control

def energy_controller_acrobat(m1, m2, L1, L2, omega1, omega2, g, theta1, theta2, E_desired, k):
    # Compute total energy for the acrobat (double pendulum)
    E1 = 0.5 * m1 * L1**2 * omega1**2 - m1 * g * L1 * np.cos(theta1)
    E2 = 0.5 * m2 * L2**2 * omega2**2 - m2 * g * L2 * np.cos(theta1 + theta2)
    E_total = E1 + E2
    
    E_tilde = E_total - E_desired
    
    return -k * omega2 * E_tilde