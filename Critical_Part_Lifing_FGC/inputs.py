import customtkinter as ctk

import customtkinter as ctk
from tkinter import LEFT

class DimensionsInputTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Add informational text at the top
        info_text = "🛈 Enter specimen and crack dimensions"
        info_label = ctk.CTkLabel(self.parent, text=info_text, wraplength=500, justify=LEFT, font=("Arial", 12))
        info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.entries = {}
        labels = {
            "width": "Width (W, in)",
            "thickness": "Thickness (T, in)",
            "hole_diameter": "Hole Diameter (D, in)",
            "initial_crack_length_A": "Initial Crack Length A (in)",
            "initial_crack_length_C": "Initial Crack Length C (in)"
        }

        for i, (key, text) in enumerate(labels.items()):
            label = ctk.CTkLabel(self.parent, text=text)
            label.grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(self.parent)
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
            self.entries[key] = entry

        self.create_navigation_buttons(len(labels) + 1)

    def create_navigation_buttons(self, row):
        self.clear_button = ctk.CTkButton(self.parent, text="Clear", command=self.clear, fg_color="#2E3092")
        self.clear_button.grid(row=row, column=0, padx=10, pady=10, sticky="e")

        self.next_button = ctk.CTkButton(self.parent, text="Next", command=lambda: self.app.show_tab("Spectrum Input"), fg_color="#2E3092")
        self.next_button.grid(row=row, column=1, padx=10, pady=10, sticky="w")

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, ctk.END)

    def get_params(self):
        return {key: float(entry.get()) for key, entry in self.entries.items()}

    def set_params(self, params):
        for key, entry in self.entries.items():
            if key in params:
                entry.delete(0, ctk.END)
                entry.insert(0, float(params[key]))


class SpectrumInputTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        
        # Add informational text with icon
        info_icon = "ℹ️"
        info_text = (f"{info_icon} Stress Multiplication Factor (SMF) multiplies the stress or load levels found "
                     "in spectrum files. This allows normalized spectra to be used. If actual stress levels are used in the spectrum files, "
                     "SMF should be set to 1.\n\n"
                     "Residual Strength Requirement (Pxx) is the value of stress (or load for models using load input) which must be carried at all crack sizes. "
                     "It is used to determine the critical crack size - if a non-zero value is entered.\n\n"
                     "Stress Preload (SPL) is used to account for pre-existing stresses. This value is added to the max and min spectrum stresses after they have been multiplied by SMF.\n\n\n")
        info_label = ctk.CTkLabel(self.parent, text=info_text, wraplength=500, justify="left")
        info_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")
        
        labels = {
            "SMF": "Stress Multiplication Factor (SMF)",
            "Pxx": "Residual Strength Requirement (Pxx)",
            "SPL": "Stress Preload (SPL)"
        }

        for i, (key, text) in enumerate(labels.items()):
            label = ctk.CTkLabel(self.parent, text=text)
            label.grid(row=i + 1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(self.parent)
            entry.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
            self.entries[key] = entry

        self.create_navigation_buttons(len(labels) + 1)

    def create_navigation_buttons(self, row):
        self.previous_button = ctk.CTkButton(self.parent, text="Previous", command=lambda: self.app.show_tab("Dimensions"), fg_color="#2E3092")
        self.previous_button.grid(row=row, column=0, padx=10, pady=10, sticky="e")

        self.clear_button = ctk.CTkButton(self.parent, text="Clear", command=self.clear, fg_color="#2E3092")
        self.clear_button.grid(row=row, column=1, padx=10, pady=10, sticky="w")

        self.next_button = ctk.CTkButton(self.parent, text="Next", command=lambda: self.app.show_tab("Walker Equation Data"), fg_color="#2E3092")
        self.next_button.grid(row=row, column=2, padx=10, pady=10, sticky="w")

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, ctk.END)

    def get_params(self):
        return {key: float(entry.get()) for key, entry in self.entries.items()}

    def set_params(self, params):
        for key, entry in self.entries.items():
            if key in params:
                entry.delete(0, ctk.END)
                entry.insert(0, float(params[key]))


class WalkerEquationInputTab:
    def __init__(self, parent, app, calculate_callback):
        self.parent = parent
        self.app = app
        self.calculate_callback = calculate_callback
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        labels = {
            "C": "C (Paris Coefficient)",
            "n": "n (Paris Exponent)",
            "m": "m (Walker Coefficient)",
            "material_name": "Material name",
            "coefficient_thermal_expansion": "Coefficient of Thermal Expansion",
            "youngs_modulus": "Young's Modulus",
            "yield_strength": "Yield Strength, YLD",
            "poissons_ratio": "Poisson's Ratio",
            "plane_stress_fracture_toughness": "Plane Stress Fracture Toughness, KC",
            "plane_strain_fracture_toughness": "Plane Strain Fracture Toughness, KIC",
            "delta_K_threshold_value": "Delta K threshold value @R=0",
            "lower_limit_R_shift": "Lower limit on R shift (0..-1)",
            "upper_limit_R_shift": "Upper limit on R shift (< 1)"
        }

        positions = {
            "C": (1, 0), "n": (1, 1), "m": (1, 2),
            "material_name": (3, 0), "coefficient_thermal_expansion": (4, 0),
            "youngs_modulus": (4, 1), "yield_strength": (5, 0),
            "poissons_ratio": (5, 1), "plane_stress_fracture_toughness": (6, 0),
            "plane_strain_fracture_toughness": (7, 1), "delta_K_threshold_value": (7, 0),
            "lower_limit_R_shift": (6, 1), "upper_limit_R_shift": (7, 1)
        }

        # Add informational text with icon
        info_icon = "ℹ️"
        info_text = f"{info_icon} The Walker equation extended the early Paris equation by allowing the shift in da/dN vs. Delta K as a function of stress ratio (R). The equation may be used in several segments to attempt to model the sigmoidal shape of the data.\n\n\n"
        info_label = ctk.CTkLabel(self.parent, text=info_text, wraplength=700, justify="left")
        info_label.grid(row=0, column=0, columnspan=5, padx=10, pady=20, sticky="w")

        for key, (row, col) in positions.items():
            label = ctk.CTkLabel(self.parent, text=labels[key])
            label.grid(row=row, column=col * 2, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(self.parent)
            entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="w")
            self.entries[key] = entry

        self.calculate_button = ctk.CTkButton(self.parent, text="Calculate", command=self.calculate_callback, fg_color="green")
        self.calculate_button.grid(row=9, column=3, columnspan=1, pady=10, sticky="ew")

        self.create_navigation_buttons(9)


    def create_navigation_buttons(self, row):
        self.previous_button = ctk.CTkButton(self.parent, text="Previous", command=lambda: self.app.show_tab("Spectrum Input"), fg_color="#2E3092")
        self.previous_button.grid(row=row, column=0, padx=10, pady=10, sticky="e")

        self.clear_button = ctk.CTkButton(self.parent, text="Clear", command=self.clear, fg_color="#2E3092")
        self.clear_button.grid(row=row, column=1, padx=10, pady=10, sticky="w")

        self.next_button = ctk.CTkButton(self.parent, text="Next", command=lambda: self.app.show_tab("Results"), fg_color="#2E3092")
        self.next_button.grid(row=row, column=2, padx=10, pady=10, sticky="w")

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, ctk.END)

    def get_params(self):
        return {key: float(entry.get()) if entry.get().replace('.', '', 1).isdigit() else entry.get() for key, entry in self.entries.items()}

    def set_params(self, params):
        for key, entry in self.entries.items():
            if key in params:
                entry.delete(0, ctk.END)
                # Convert to float if the value should be numeric
                if key in ["C", "n", "m", "plane_stress_fracture_toughness", "plane_strain_fracture_toughness", "delta_K_threshold_value", "lower_limit_R_shift", "upper_limit_R_shift", "coefficient_thermal_expansion"]:
                    entry.insert(0, float(params[key]))
                else:
                    entry.insert(0, params[key])
