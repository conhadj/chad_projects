# data.py
class InputData:
    def __init__(self):
        self.num_sets = 1
        self.c_values = []
        self.n_values = []
        self.m_values = []
        
        self.material_name = ""
        self.coefficient_of_thermal_expansion = 0
        self.youngs_modulus = 0
        self.yield_strength = 0
        self.poissons_ratio = 0
        self.plane_stress_fracture_toughness = 0
        self.plane_strain_fracture_toughness = 0
        self.delta_k_threshold = 0
        self.lower_limit_r_shift = 0
        self.upper_limit_r_shift = 0
        
        self.failure_cycles = 0
        self.final_crack_size = 0
