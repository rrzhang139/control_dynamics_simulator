import numpy as np

def euler_step(func, t, state, u, dt):
    """ Implements one step of Euler integration. """
    derivative = np.array(func(t, state, u))
    return state + derivative * dt


def rk4_step(func, t, state, u, dt):
    """ Implements one step of RK4 integration. """
    k1 = np.array(func(t, state, u)) * dt
    k2 = np.array(func(t + dt/2, state + k1/2, u)) * dt
    k3 = np.array(func(t + dt/2, state + k2/2, u)) * dt
    k4 = np.array(func(t + dt, state + k3, u)) * dt
    return state + (k1 + 2*k2 + 2*k3 + k4) / 6