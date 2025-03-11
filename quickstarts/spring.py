import numpy as np
import matplotlib.pyplot as plt

# Constants
dt = 0.1  # Time step
T = 100     # Total simulation time
steps = int(T / dt)  # Number of iterations
m = 1.0    # Mass
k = 1.0    # Spring constant
b = 0.5

# Initial conditions
x = 1.0    # Initial position
v = 0.0    # Initial velocity

# Storage for results
positions = []
times = np.arange(0, T, dt)

# Setup animation before simulation
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.5, 0.5)

# Mass representation
mass, = plt.plot([], [], 'bo', markersize=14)  # Blue ball for mass
spring, = plt.plot([], [], 'k-', lw=2)  # Spring line

# Function to update the animation during debugging
def update_animation(x_pos):
    mass.set_data(x_pos, 0)  # Update mass position
    spring.set_data([-1.5, x_pos], [0, 0])  # Spring from left to mass
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)  # Small pause to allow animation to update

# In charge of making the plots! 

# Show initial state
plt.ion()  # Turn on interactive mode
plt.title("Mass-Spring System Animation (Debug Mode)")
update_animation(x) # We initialize the plots with initial position, mass etc

# Loop through each time. Calculate the mass using 

# Euler Integration with animation updates
for t in times:
    # breakpoint()  # Debugger will stop here
    a = (-k * x - b * v) / m  # Compute acceleration (Hooke's Law)
    v = v + a * dt  # Update velocity (first integration)
    x = x + v * dt  # Update position (second integration)
    
    positions.append(x)  # Store position
    update_animation(x)  # Update animation at each step

# Keep the plot open when done
plt.ioff()  # Turn off interactive mode
plt.show(block=True)
