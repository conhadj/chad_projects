import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from inputs import DimensionsInputTab, SpectrumInputTab, WalkerEquationInputTab
from results import ResultTab
import json
from calculations import calculate_crack_growth  # Ensure this import is present

class CrackGrowthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Crack Growth Analysis")
        self.geometry("800x600")

        self.create_menu()

        self.tab_view = ctk.CTkTabview(self, width=800, height=200)
        self.tab_view.pack(expand=1, fill="both")
        
        self.tabs = {}
        self.tabs["Dimensions"] = DimensionsInputTab(self.tab_view.add("Dimensions"), self)
        self.tabs["Spectrum Input"] = SpectrumInputTab(self.tab_view.add("Spectrum Input"), self)
        self.tabs["Walker Equation Data"] = WalkerEquationInputTab(self.tab_view.add("Walker Equation Data"), self, self.calculate)
        self.tabs["Results"] = ResultTab(self.tab_view.add("Results"), self)

    def create_menu(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        theme_menu = tk.Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Light Mode", command=lambda: ctk.set_appearance_mode("light"))
        theme_menu.add_command(label="Dark Mode", command=lambda: ctk.set_appearance_mode("dark"))
        menu_bar.add_cascade(label="Theme", menu=theme_menu)

        self.config(menu=menu_bar)

    def show_tab(self, tab_name):
        self.tab_view.set(tab_name)

    def calculate(self):
        params = {}
        for tab_name, tab in self.tabs.items():
            if tab_name != "Results":  # Skip Results tab for parameter collection
                params.update(tab.get_params())

        # Convert only numerical parameters to float
        for key in params:
            if key != "material_name":  # assuming material_name should remain a string
                try:
                    params[key] = float(params[key])
                except ValueError:
                    pass

        cycle_counts, crack_lengths_A, crack_lengths_C, crack_areas = calculate_crack_growth(params)
        self.tabs["Results"].display_results(cycle_counts, crack_lengths_A, crack_lengths_C, crack_areas)
        self.show_tab("Results")

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for tab_name, tab in self.tabs.items():
                    if tab_name != "Results":  # Skip Results tab for setting parameters
                        tab.set_params(data)

    def export_data(self):
        params = {}
        for tab_name, tab in self.tabs.items():
            if tab_name != "Results":  # Skip Results tab for parameter collection
                params.update(tab.get_params())
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(params, file)

if __name__ == "__main__":
    app = CrackGrowthApp()
    app.mainloop()
