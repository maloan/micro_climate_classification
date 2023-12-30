### README for Urban Microclimate Classification Project

#### Overview  
This repository contains the source code for the "Urban Microclimate Classification Project," focusing on the analysis of urban balcony microclimates. The project's aim is to categorize these microclimates based on temperature and solar radiation data, thereby enabling personalized plant recommendations in urban settings.

#### Project Structure  
This project is organized into several directories, each serving a specific purpose in the research workflow:

- `API_and_Data/`: Contains scripts for interacting with various APIs and handling data retrieval and preprocessing. This includes scripts for the Boum and FYTA APIs, data fetching, and historical weather data processing.

- `clustering_new_data/`: This directory houses the code for the clustering algorithms, including the GUI, main script, and user interaction modules. It also contains the requirements file for setting up the project environment.

- `data/`: Stores all the collected and processed data, including historical weather data, survey data, and various dataframes in CSV and pickled formats.

- `main_project/`: Features the primary Jupyter notebook (`data_processing_and_clustering.ipynb`) that encapsulates the entire data processing and clustering process.

- `model/`: Contains the saved models and scalers used in the project, such as KMeans models for temperature and radiation, along with their respective scalers.

- `msc/`: Includes additional scripts for temperature error correction, data visualization, and mathematical computations relevant to the study.

- `plots/`: A directory for storing generated plots and visualizations.

- `tests/`: Contains unit tests for various components of the project, ensuring the reliability and accuracy of the code.

#### Getting Started  
1. Clone this repository to your local machine:  
```  
git clone https://github.com/maloan/micro_climate_classification.git  
```  

2. Navigate to the `clustering_new_data/` directory and install the required dependencies:  
```  
pip install -r requirements.txt  
```

#### Usage  
To run the project, follow these steps based on the specific aspect you're interested in:
1. **Data Analysis and Clustering**: Execute the `data_processing_and_clustering.ipynb` notebook in the `main_project/` directory.
2. **Categorizing a new Microclimate**: Execute the `main.py` program in the `clustering_new_data/` directory.

#### Contributing  
If you're interested in contributing to this project, please feel free to fork the repository, create your feature branch, and submit a pull request.

#### License  
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

#### Contact  
- Project Maintainer: Ananda Kurth - ananda.kurth@unifr.ch  
- Project Link: https://github.com/maloan/micro_climate_classification
