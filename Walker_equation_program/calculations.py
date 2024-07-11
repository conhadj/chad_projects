def calculate_failure(data):
    total_failure_cycles = 0
    total_final_crack_size = 0

    for i in range(data.num_sets):
        c = data.c_values[i]
        n = data.n_values[i]
        m = data.m_values[i]
        
        # Calculating delta K
        delta_k = data.plane_stress_fracture_toughness - data.delta_k_threshold
        
        # Calculating stress ratio R
        stress_ratio = data.lower_limit_r_shift / data.upper_limit_r_shift if data.upper_limit_r_shift != 0 else 0.5  # Assuming 0.5 if upper_limit_r_shift is zero

        # Calculating the crack growth rate using the Walker equation
        crack_growth_rate = c * (delta_k * (1 - stress_ratio)**(m - 1))**n
        
        # Calculate the number of cycles to failure for this set
        # Walker equation gives da/dN, dividing delta K threshold by crack growth rate gives failure cycles
        failure_cycles = data.delta_k_threshold / crack_growth_rate
        total_failure_cycles += failure_cycles

        # Calculate the final crack size for this set
        # Multiplying the crack growth rate by the number of cycles to failure gives the final crack size
        final_crack_size = crack_growth_rate * failure_cycles
        total_final_crack_size += final_crack_size

    return total_failure_cycles, total_final_crack_size
