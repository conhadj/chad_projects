# Crack Growth Analysis Software

## Overview

This project aims to recreate the functionality of the AFGROW software, a fatigue crack growth prediction program developed by the United States Air Force. AFGROW uses linear elastic fracture mechanics (LEFM) to determine the crack growth rate and cycles to failure of a two-dimensional cross-section with a given crack. The software includes a library of predefined cross-sections and material properties and allows users to define their own. It incorporates several crack growth rate models, including the Walker and Paris equations, and accounts for both crack closure and residual stress effects.

The goal of this project is to provide a similar tool for analyzing crack growth in materials under cyclic loading. The software uses the Walker equation to account for the effect of the stress ratio on crack growth rate and provides a user-friendly interface for inputting parameters and viewing results.

## Key Concepts

### Cyclic Loading and Stress Intensity Factor

- **Cyclic Loading**: Repeated application of load or stress on a material. The parameters include maximum stress ($\sigma_{\text{max}}$), minimum stress ($\sigma_{\text{min}}$), mean stress ($\sigma_m$), stress amplitude ($\sigma_a$), and stress range ($\Delta\sigma$).
- **Stress Ratio ($R$)**: Ratio of minimum stress to maximum stress: 
  $$R = \frac{\sigma_{\text{min}}}{\sigma_{\text{max}}}$$
- **Stress Intensity Factor**: A function of geometry and applied stress, representing the stress state near the crack tip.
  $$K_{\text{max}} = Y \sigma_{\text{max}} \sqrt{\pi a}$$
  $$K_{\text{min}} = Y \sigma_{\text{min}} \sqrt{\pi a}$$
  $$\Delta K = K_{\text{max}} - K_{\text{min}}$$

### Crack Growth Rate

- **Walker Equation**: Generalization of the Paris equation to account for the effect of stress ratio $R$ on crack growth rate.
  $$\frac{da}{dN} = C \left( \Delta K (1 - R)^{m-1} \right)^n$$
  Where $C$, $n$, and $m$ are material constants, and $\Delta K$ is the stress intensity range.

### Crack Growth Simulation

- **Simulation Loop**: The crack growth simulation runs over a specified number of cycles, recalculating the crack growth rate and updating the crack lengths and areas.
- **Stopping Criteria**: The simulation stops if the crack growth rate is very small, the crack area becomes unreasonably large, or the maximum number of cycles is reached.

## Goals and Functionality

The primary goal of this software is to provide a robust and user-friendly tool for predicting fatigue crack growth in materials under cyclic loading. Key features include:

- **Parameter Input**: Users can input various parameters such as initial crack lengths, material properties, and loading conditions.
- **Walker Equation Implementation**: The software uses the Walker equation to model crack growth, accounting for the effect of stress ratio.
- **Simulation and Results**: The software simulates crack growth over a specified number of cycles and displays the results, including crack lengths, crack areas, and the number of cycles to failure.

## Usage

1. **Input Parameters**: Enter the required parameters such as initial crack lengths, stress intensity factors, material properties, etc.
2. **Run Simulation**: Click the "Calculate" button to run the simulation.
3. **View Results**: The results, including crack lengths, crack areas, and cycle counts, are displayed in the Results tab. Users can also export the results to a JSON file.

## Example

An example simulation for a titanium plate with a center hole under cyclic tension can be performed by inputting the relevant parameters and running the simulation. The software will predict the number of cycles to failure and provide detailed plots of crack growth over time.

## Installation

### Prerequisites

- Git should be installed on your machine. You can download it from [here](https://git-scm.com/).

### Cloning the Specific Project Folder

To clone only the specific project folder from the repository, follow these steps:

1. **Initialize a Sparse Checkout**:
   - Open a terminal or command prompt and navigate to the directory where you want to clone the project.
   - Initialize a new Git repository.
     ```sh
     git init
     ```

2. **Set Sparse Checkout Configuration**:
   - Enable the sparse-checkout feature.
     ```sh
     git config core.sparseCheckout true
     ```

3. **Define the Folder to be Checked Out**:
   - Define the project's folder to check out.
     ```sh
     echo "Critical_Part_Lifing_FGC/" >> .git/info/sparse-checkout
     ```

4. **Add Remote Repository**:
   - Add the remote repository URL.
     ```sh
     git remote add -f origin https://github.com/conhadj/chad_projects.git
     ```

5. **Pull the Specific Folder**:
   - Pull the specified folder from the repository.
     ```sh
     git pull origin main
     ```

### Running the Executable

To run the program on your local machine, follow these steps:

1. **Navigate to the Executable Directory**:
   - Open a terminal or command prompt and navigate to the `executable` directory inside the cloned project folder.
     ```sh
     cd Critical_Part_Lifing_FGC/executable
     ```

2. **Run the Executable**:
   - Locate the `.exe` file inside the `executable` folder. Double-click on the `.exe` file to run the program.
     - **Windows**: Simply double-click the `CrackGrowthAnalysis.exe` file.
     - **Command Line**: Alternatively, you can run it from the command line.
       ```sh
       CrackGrowthAnalysis.exe
       ```

### Notes

- **Dependencies**: The executable includes all necessary dependencies and should run without any additional installations.
<!-- - **Troubleshooting**: If you encounter any issues while running the executable, please check the [Issues](https://github.com/yourusername/your-repo-name/issues) section of the repository or contact us for support.

## Contributing

[Provide information on how others can contribute to your project.]

## License

[Include license information here.] -->
