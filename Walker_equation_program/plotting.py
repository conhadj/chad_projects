# plotting.py
import matplotlib.pyplot as plt

def plot_results(data):
    # Example plotting logic
    cycles = range(1, int(data.failure_cycles) + 1)
    crack_sizes = [data.c_value * (data.max_stress ** data.m_value) * (1 - (data.min_stress / data.max_stress) ** data.n_value) * cycle for cycle in cycles]
    
    plt.figure()
    plt.plot(cycles, crack_sizes)
    plt.xlabel('Cycles')
    plt.ylabel('Crack Length')
    plt.title('Crack Length vs. Cycles')
    plt.grid(True)
    plt.show()