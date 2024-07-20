import numpy as np

def calculate_crack_growth(params):
    # Ensure all parameters are converted to appropriate numeric types
    C = float(params["C"])
    n = float(params["n"])
    m = float(params["m"])
    initial_crack_length_A = float(params["initial_crack_length_A"])
    initial_crack_length_C = float(params["initial_crack_length_C"])
    SMF = float(params["SMF"])
    stress_ratio = 0  # R
    block_size = 10  # Number of cycles after which crack growth is recalculated
    max_cycles = 50000  # Maximum number of cycles for the simulation

    width = float(params["width"])
    thickness = float(params["thickness"])
    hole_diameter = float(params["hole_diameter"])

    plane_stress_fracture_toughness = float(params["plane_stress_fracture_toughness"])
    plane_strain_fracture_toughness = float(params["plane_strain_fracture_toughness"])
    delta_K_threshold_value = float(params["delta_K_threshold_value"])

    def walker_equation(delta_K, R, C, n, m):
        try:
            return C * (delta_K * (1 - R) ** (m - 1)) ** n
        except OverflowError:
            return float('inf')

    def calculate_delta_K(SMF, crack_length_A, crack_length_C, width, hole_diameter):
        a = (crack_length_A + crack_length_C) / 2  # Average crack length
        beta = 1 + 0.5 * (hole_diameter / width)
        K_max = SMF * np.sqrt(np.pi * a) * beta  # Adjusted with geometry factor
        return K_max  # Delta K in ksi√in

    crack_length_A = initial_crack_length_A
    crack_length_C = initial_crack_length_C
    crack_area = crack_length_A * crack_length_C
    cycles = 0
    crack_areas = [crack_area]
    crack_lengths_A = [crack_length_A]
    crack_lengths_C = [crack_length_C]
    cycle_counts = [cycles]

    while cycles < max_cycles:
        delta_K = calculate_delta_K(SMF, crack_length_A, crack_length_C, width, hole_diameter)
        if delta_K < delta_K_threshold_value:  # If delta_K is below threshold, no crack growth
            break
        da_dN = walker_equation(delta_K, stress_ratio, C, n, m)
        crack_growth = da_dN * block_size
        if crack_growth < 1e-9:  # If crack growth rate is very small, stop the simulation
            break
        crack_length_A += crack_growth / 2
        crack_length_C += crack_growth / 2
        crack_area = crack_length_A * crack_length_C
        if crack_area > 1.0:  # Stop if the crack area becomes unreasonably large
            break

        cycles += block_size
        crack_areas.append(crack_area)
        crack_lengths_A.append(crack_length_A)
        crack_lengths_C.append(crack_length_C)
        cycle_counts.append(cycles)

    return cycle_counts, crack_lengths_A, crack_lengths_C, crack_areas
