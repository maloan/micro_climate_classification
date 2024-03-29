# Microclimate Predictor Application 

## Overview

The microclimate prediction application is a tool that predicts the temperature and radiation clusters of new locations. This application is made up of several modules and classes that gather and analyze data that has been collected over at least one week. It is important to note that the accuracy of the prediction increases with the duration of data collection. This Python-based application integrates data fetching, processing, and machine learning algorithms to provide clustering of environmental data. It is structured with a user-friendly GUI for easy data input and robust backend processing for accurate predictions.

## Features

- **Interface**: Built with Tkinter, the GUI allows for seamless data entry and interaction.
- **Data Fetching**: Integrates with APIs like Boum API and OpenWeatherMap API for real-time data retrieval.
- **Advanced Data Processing**: Includes data preprocessing, cleaning, and organizing classes.
- **Cluster Prediction**: Utilizes machine learning models for predicting temperature and radiation clusters.
- **Informative Cluster Reporting**: Offers detailed insights into the identified clusters, categorizing data effectively.

## System Requirements

- Python 3.x
- numpy, pandas, matplotlib, seaborn, scipy, boum, tqdm, requests, geopy, joblib (libraries) 
- Access to the Internet for API communication

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/maloan/micro_climate_classification/clustering_new_data
   ```
2. Install required Python libraries:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application by running the `microclimate_predictor.py` script.
2. Enter the required data in the GUI fields.
3. Submit the data for processing and prediction.
4. View the predicted temperature and radiation clusters in the output.

## Components

- **microclimate_predictor.py**: Main script with GUI initialization and application control flow.
- **ClusterPredictor**: Class for preprocessing and predicting clusters using trained models.
- **DataFetcher**: Class for fetching data from external APIs.
- **DataPreprocessor & DataProcessor**: Data cleaning, correction, and organization classes.
- **UserInputGUI**: Tkinter-based class for handling user input.
- **Config.py**: Script for defining essential application constants.
- **ClusterInformation**: Class for interpreting and displaying cluster information.
- **requirements.txt*: File including the required dependencies.


#### License  
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

#### Contact  
- Project Maintainer: Ananda Kurth - ananda.kurth@unifr.ch  
- Project Link: https://github.com/maloan/micro_climate_classification
