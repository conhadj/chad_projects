import customtkinter as ctk
from calculations import calculate_crack_growth
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ResultTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        self.result_label = ctk.CTkLabel(self.parent, text="Results will be displayed here.")
        self.result_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.fig1, self.ax1 = plt.subplots(figsize=(5, 4))  # Adjust figure size
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.parent)
        self.canvas1.get_tk_widget().grid(row=1, column=0, pady=10, padx=15, sticky="nsew")

        self.fig2, self.ax2 = plt.subplots(figsize=(5, 4))  # Adjust figure size
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.parent)
        self.canvas2.get_tk_widget().grid(row=1, column=1, pady=10, padx=15, sticky="nsew")

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        button_frame = ctk.CTkFrame(self.parent)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self.previous_button = ctk.CTkButton(button_frame, text="Previous", command=lambda: self.app.show_tab("Walker Equation Data"), fg_color="#2E3092")
        self.previous_button.pack(side=ctk.LEFT, padx=10)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear, fg_color="#2E3092")
        self.clear_button.pack(side=ctk.LEFT, padx=10)

    def display_results(self, cycle_counts, crack_lengths_A, crack_lengths_C, crack_areas):
        self.ax1.clear()
        self.ax2.clear()

        self.ax1.plot(cycle_counts, crack_lengths_A, label='Crack Length A')
        self.ax1.plot(cycle_counts, crack_lengths_C, label='Crack Length C')
        self.ax1.set_xlabel('Cycles')
        self.ax1.set_ylabel('Crack Length (inches)')
        self.ax1.set_title('Crack Length vs. Cycles')
        self.ax1.legend()
        self.ax1.grid(True)

        self.ax2.plot(cycle_counts, crack_areas, label='Crack Area')
        self.ax2.set_xlabel('Cycles')
        self.ax2.set_ylabel('Crack Area (square inches)')
        self.ax2.set_title('Crack Area vs. Cycles')
        self.ax2.legend()
        self.ax2.grid(True)

        self.canvas1.draw()
        self.canvas2.draw()

        self.result_label.configure(text=f"Final crack length A: {crack_lengths_A[-1]:.6f} inches\n"
                                         f"Final crack length C: {crack_lengths_C[-1]:.6f} inches\n"
                                         f"Final crack area: {crack_areas[-1]:.6f} square inches\n"
                                         f"Total cycles: {cycle_counts[-1]}")

    def clear(self):
        self.result_label.configure(text="Results will be displayed here.")
        self.ax1.clear()
        self.ax2.clear()
        self.canvas1.draw()
        self.canvas2.draw()
