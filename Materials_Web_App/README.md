
# Materials And Mechanical Properties Dashboard, EDA and Machine Learning Model Training with Python – Streamlit

Interactive dashboard built-in Python and the Streamlit library to visualize, analyze data related to materials and their mechanical properties and train machine learning models.

## Deployment

The app is deployed on Google Cloud Platform Services and can be accessed via
https://streamlit-materials-app.nw.r.appspot.com

## Run the app
```Powershell
# vanilla terminal
streamlit run 🏠_Main.py

# quit
ctrl-c
```

## Dataset Overview

This dataset contains information about various materials and their mechanical properties. It was sourced from Kaggle and can be found [here](https://www.kaggle.com/datasets/purushottamnawale/materials?select=material.csv).

The dataset includes the following columns:

- **Material**: The name of the material.
- **Su**: Ultimate tensile strength (in MPa).
- **Sy**: Yield strength (in MPa).
- **E**: Modulus of elasticity (in MPa).
- **G**: Shear modulus (in MPa).
- **μ**: Poisson's ratio.
- **ρ**: Density (in g/cm³).

## Usage

This dataset was originally used to train machine learning models for predicting the suitability of materials for being used for an Electric Vehicle chasis. It can also be used for educational purposes to understand the relationships between different mechanical properties of materials.


## Data Source

The dataset was created by Purushottam Nawale and is part of the research presented in the paper "Design automation and CAD customization of an EV chassis". The paper can be accessed [here](https://www.myaidrive.com/file-gnicXf9UT9UQf1n4gp6QxRDY).

## Citation

```latex
@article{nawale2023design,
  title={Design automation and CAD customization of an EV chassis},
  author={Purushottam Nawale, Akshay Kanade, Bhalchandra Nannaware, Abhijeet Sagalgile, Nagesh Chougule, Abhishek Patange},
  journal={Journal of Physics: Conference Series},
  volume={2601},
  pages={012014},
  year={2023},
  publisher={IOP Publishing},
  doi={10.1088/1742-6596/2601/1/012014}
}


