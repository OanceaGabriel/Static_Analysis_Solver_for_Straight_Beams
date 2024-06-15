import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrow, Rectangle


class BeamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beam Points Drawer")

        self.points = []
        self.file_path = None  # New variable to store the file path

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.load_button = ttk.Button(self.main_frame, text="Load Points from File", command=self.load_points)
        self.load_button.grid(row=0, column=0, columnspan=2, pady=5)

        self.draw_button = ttk.Button(self.main_frame, text="Draw Beam", command=self.draw_beam)
        self.draw_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.points_listbox = tk.Listbox(self.main_frame, height=10, width=70)
        self.points_listbox.grid(row=2, column=0, columnspan=2, pady=10)

        self.clear_button = ttk.Button(self.main_frame, text="Clear Points", command=self.clear_points)
        self.clear_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.next_step_button = ttk.Button(self.main_frame, text="Next Step", command=self.next_step)
        self.next_step_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.next_step_button.config(state=tk.DISABLED)  # Initially disabled

    def load_points(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not self.file_path:
            return
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                self.points.clear()
                self.points_listbox.delete(0, tk.END)
                for line in lines[1:]:  # Skip the first line
                    name, x, support, force, moment, dist_force = line.strip().split(';')
                    point = {
                        'name': name,
                        'x': float(x),
                        'support': support,
                        'force': float(force),
                        'moment': float(moment),
                        'dist_force': float(dist_force)
                    }
                    self.points.append(point)
                    self.points_listbox.insert(tk.END,
                                               f"Point: {name}, x: {x}, support: {support}, force: {force}, moment: {moment}, dist_force: {dist_force}")
        except Exception as e:
            messagebox.showerror("File Error", f"Error reading file: {e}")

    def draw_beam(self):
        if not self.points:
            messagebox.showerror("Input Error", "Please load points from a file first.")
            return

        x_values = [point['x'] for point in self.points]
        y_values = [0 for _ in self.points]
        labels = [point['name'] for point in self.points]
        forces = [point['force'] for point in self.points]
        moments = [point['moment'] for point in self.points]
        dist_forces = [point['dist_force'] for point in self.points]

        plt.figure()
        plt.plot(x_values, y_values, marker='o', linestyle='-', color='black', linewidth=5)  # Added line-width=5 here

        arrow_length = 0.1
        for i, (x, y, dist_force) in enumerate(zip(x_values, y_values, dist_forces)):
            if dist_force != 0:
                arrow_length = 0.1
                arrow_color = 'skyblue'
                arrow_y = 0.1 if dist_force > 0 else -0.1
                arrow_direction = -1 if dist_force > 0 else 1
                arrow = FancyArrow(x, arrow_y, 0, arrow_direction * (arrow_length - 0.06), width=0.01,
                                   head_width=0.1, head_length=0.05, color=arrow_color)
                plt.gca().add_patch(arrow)

        for i in range(len(self.points) - 1):
            x1, x2 = x_values[i], x_values[i + 1]
            dist_force1, dist_force2 = dist_forces[i], dist_forces[i + 1]

            # Draw a rectangle between two consecutive points if both have non-zero distributed forces
            if dist_force1 != 0 and dist_force2 != 0:
                width = abs(x2 - x1)
                height = arrow_length  # Adjust the height of the rectangle as needed
                rect_x = min(x1, x2)
                rect_y = 0 if dist_force1 > 0 else -height  # Position below the beam
                color = 'skyblue'  # Color of the rectangle
                rect = Rectangle((rect_x, rect_y), width, height, color=color, alpha=0.6, linewidth=2)
                plt.gca().add_patch(rect)

        for x, y, moment, label in zip(x_values, y_values, moments, labels):
            if moment != 0:
                radius = 0.15  # Radius of the semicircle
                center = (x, y)  # Center of the semicircle shifted to the left of the point
                start_angle = 90  # Starting angle for the semicircle
                color = 'r'  # Color of the semicircle
                arc = Arc(center, radius * 2, radius * 2, angle=0, theta1=start_angle, theta2=start_angle + 180,
                          color=color, lw=2)
                plt.gca().add_patch(arc)
                plt.text(x, radius + 0.05, f"{moment}Nm", ha='center')

                # Adding arrows at the ends of the semicircle
                arrow_length = 0.01
                if moment < 0:
                    arrow = FancyArrow(x, - radius, -arrow_length, 0, head_width=0.05, head_length=0.05, color=color)
                else:
                    arrow = FancyArrow(x, radius, arrow_length, 0, head_width=0.05, head_length=0.05, color=color)
                plt.gca().add_patch(arrow)

            # Add green arrow with label "y" + [name] for points with names as letters
            if label.isalpha():
                green_arrow_length = 0.1
                arrow_label = "y" + label
                arrow_x = x  # Vertical arrow directly under the point
                arrow_y = -0.3  # Position below the beam
                arrow = FancyArrow(arrow_x, arrow_y, 0, green_arrow_length, width=0.01, head_width=0.1,
                                   head_length=0.05, color='g')
                plt.gca().add_patch(arrow)
                plt.text(arrow_x, arrow_y - 0.05, arrow_label, color='g', ha='center', fontsize=16)

        for i, (x, y, label, force) in enumerate(zip(x_values, y_values, labels, forces)):
            plt.text(x, y - 0.1, label, ha='center')
            if force != 0:
                arrow_direction = 0.2 if force > 0 else -0.2
                plt.arrow(x, y, 0, arrow_direction, width=0.01, head_width=0.1, head_length=0.05, fc='r', ec='r')
                plt.text(x, y + arrow_direction + 0.1, f"{force}N", ha='center')

        plt.title("Beam Points")
        plt.xlabel("x")
        plt.ylabel("Beam")
        plt.ylim(-0.5, 0.5)
        plt.grid(False)
        plt.show()

        self.next_step_button.config(state=tk.NORMAL)  # Enable the "Next Step" button after drawing

    def clear_points(self):
        self.points.clear()
        self.points_listbox.delete(0, tk.END)
        self.next_step_button.config(state=tk.DISABLED)  # Disable the "Next Step" button when points are cleared

    def next_step(self):
        if self.file_path:
            print(f"Continuing with file: {self.file_path}")
            # Here you can add logic to continue with the next step using self.file_path
        else:
            print("No file loaded yet")

        self.root.destroy()  # Close the main window to proceed with the next step
