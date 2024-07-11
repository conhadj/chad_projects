# ui.py
import customtkinter as ctk
from data import InputData
from calculations import calculate_failure
from plotting import plot_results

class MainUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.data = InputData()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Walker Equation Data Section
        self.walker_data_frame = ctk.CTkFrame(self)
        self.walker_data_frame.pack(pady=10)
        
        ctk.CTkLabel(self.walker_data_frame, text="Walker Equation Data").grid(row=0, column=0, columnspan=3)
        
        self.num_sets = ctk.CTkComboBox(self.walker_data_frame, values=["1", "2", "3", "4", "5"])
        self.num_sets.grid(row=1, column=0)
        self.num_sets.set("1")
        
        self.c_values = [ctk.CTkEntry(self.walker_data_frame, placeholder_text=f"C{i+1}") for i in range(5)]
        self.n_values = [ctk.CTkEntry(self.walker_data_frame, placeholder_text=f"n{i+1}") for i in range(5)]
        self.m_values = [ctk.CTkEntry(self.walker_data_frame, placeholder_text=f"m{i+1}") for i in range(5)]
        
        for i in range(5):
            self.c_values[i].grid(row=2+i, column=0)
            self.n_values[i].grid(row=2+i, column=1)
            self.m_values[i].grid(row=2+i, column=2)
        
        # Material Properties Section
        self.material_properties_frame = ctk.CTkFrame(self)
        self.material_properties_frame.pack(pady=10)
        
        ctk.CTkLabel(self.material_properties_frame, text="Material Properties").grid(row=0, column=0, columnspan=2)

        entry_width = 300 
        
        self.material_name = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Material Name", width=entry_width*2)
        self.coefficient_of_thermal_expansion = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Coefficient of Thermal Expansion", width=entry_width)
        self.youngs_modulus = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Young's Modulus", width=entry_width)
        self.yield_strength = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Yield Strength", width=entry_width)
        self.poissons_ratio = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Poisson's Ratio", width=entry_width)
        self.plane_stress_fracture_toughness = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Plane Stress Fracture Toughness, Kc", width=entry_width)
        self.plane_strain_fracture_toughness = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Plane Strain Fracture Toughness, KIC", width=entry_width)
        self.delta_k_threshold = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Delta K threshold value @ R=0", width=entry_width)
        self.lower_limit_r_shift = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Lower limit on R shift [0, -1]", width=entry_width)
        self.upper_limit_r_shift = ctk.CTkEntry(self.material_properties_frame, placeholder_text="Upper limit on R shift (<1)", width=entry_width)
        
        self.material_name.grid(row=1, column=0, columnspan=2)
        self.coefficient_of_thermal_expansion.grid(row=2, column=0)
        self.youngs_modulus.grid(row=2, column=1)
        self.yield_strength.grid(row=3, column=0)
        self.poissons_ratio.grid(row=3, column=1)
        self.plane_stress_fracture_toughness.grid(row=4, column=0)
        self.plane_strain_fracture_toughness.grid(row=5, column=0)
        self.delta_k_threshold.grid(row=6, column=0)
        self.lower_limit_r_shift.grid(row=5, column=1)
        self.upper_limit_r_shift.grid(row=6, column=1)
        
        # Buttons for actions
        self.calculate_button = ctk.CTkButton(self, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)
        
        self.plot_button = ctk.CTkButton(self, text="Plot Results", command=self.plot_results)
        self.plot_button.pack(pady=10)
    
    def calculate(self):
        # Get user input and store it in the data object
        self.data.num_sets = int(self.num_sets.get())
        
        self.data.c_values = [float(self.c_values[i].get()) if self.c_values[i].get() else 0 for i in range(self.data.num_sets)]
        self.data.n_values = [float(self.n_values[i].get()) if self.n_values[i].get() else 0 for i in range(self.data.num_sets)]
        self.data.m_values = [float(self.m_values[i].get()) if self.m_values[i].get() else 0 for i in range(self.data.num_sets)]
        
        self.data.material_name = self.material_name.get()
        self.data.coefficient_of_thermal_expansion = float(self.coefficient_of_thermal_expansion.get())
        self.data.youngs_modulus = float(self.youngs_modulus.get())
        self.data.yield_strength = float(self.yield_strength.get())
        self.data.poissons_ratio = float(self.poissons_ratio.get())
        self.data.plane_stress_fracture_toughness = float(self.plane_stress_fracture_toughness.get())
        self.data.plane_strain_fracture_toughness = float(self.plane_strain_fracture_toughness.get())
        self.data.delta_k_threshold = float(self.delta_k_threshold.get())
        self.data.lower_limit_r_shift = float(self.lower_limit_r_shift.get())
        self.data.upper_limit_r_shift = float(self.upper_limit_r_shift.get())
        
        # Perform calculations
        self.data.failure_cycles, self.data.final_crack_size = calculate_failure(self.data)
        
        ctk.CTkLabel(self, text=f"Component will fail in {self.data.failure_cycles} cycles with a final crack size of {self.data.final_crack_size} square inches").pack(pady=10)
    
    def plot_results(self):
        plot_results(self.data)
