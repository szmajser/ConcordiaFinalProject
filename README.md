# Snow / Rain / Hail Probability Prediction App

This project is an interactive **Streamlit** application built in **Python** to predict the **probability of Snow / Rain / Hail** using historical weather data and current forecasts. It leverages a machine learning model trained on data retrieved from the [Open-Meteo](https://open-meteo.com/en/docs) API.

## Objective

To develop a system that automatically estimates the likelihood of hail in Quebec location by combining real-time weather data and machine learning techniques.

## Dataset

Weather data was retrieved using the Open-Meteo API (`hourly` endpoint), including the following variables:
- Temperature
- Precipitation
- Relative Humidity
- Dew Point
- Weather Code 

## Modeling

Classification models tested:
- Random Forest
- Logistic Regression
- SVM

`GridSearchCV` was used for hyperparameter tuning, and a **multi-label classification** approach was applied to detect:
- Rain
- Snow
- Hail

### Evaluation Metrics:
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

## Modeling

Project Folders:
- App - App Files
- Data - CSV Generated 
- Model - Model generated to be used in the App
- Ppt - Powerpoint Presentation
- Scripts - Scripts used to retrieve historical and actual weather forecast

## Streamlit App

The web app allows users to:
- Visualize current weather data for a given location
- Predict weather conditions (rain, snow, hail)
