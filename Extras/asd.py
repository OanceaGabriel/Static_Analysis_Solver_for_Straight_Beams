import numpy as np
import matplotlib.pyplot as plt

# Define the coordinates of the line
X1, Y1 = 10, 0
X2, Y2 = 17, 13

# Generate x values for the line
x_line = np.array([X1, X2])

# Generate y values for the line
y_line = np.array([Y1, Y2])

# Plot the line
plt.plot(x_line, y_line, 'r-', label='Line')

# Fill between the line and the Y-axis
plt.fill_betweenx(y_line, 15, x_line, color='green', alpha=0.5)

# Add labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Fill Between Y-axis and a Line')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()