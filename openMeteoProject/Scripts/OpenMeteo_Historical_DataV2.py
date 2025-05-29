import pandas as pd
import requests_cache
import openmeteo_requests
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
params = {
	#"latitude": -34.6037,  #Buenos Aires
	"latitude": 52.52,      #Quebec
    #"longitude": -58.3816, #Buenos Aires
	"longitude": 13.41,     #Quebec
	"start_date": "2023-01-01",
    "end_date": "2024-12-31",
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
	"hourly": ["temperature_2m", "weather_code", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "pressure_msl", "cloud_cover", "surface_pressure", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "evapotranspiration", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_180m", "wind_direction_120m", "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm"]
}
responses = openmeteo.weather_api(url, params=params)

response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(3).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(4).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(5).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(6).ValuesAsNumpy()
hourly_pressure_msl = hourly.Variables(7).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(8).ValuesAsNumpy()
hourly_surface_pressure = hourly.Variables(9).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(10).ValuesAsNumpy()
hourly_cloud_cover_mid = hourly.Variables(11).ValuesAsNumpy()
hourly_cloud_cover_high = hourly.Variables(12).ValuesAsNumpy()
hourly_visibility = hourly.Variables(13).ValuesAsNumpy()
hourly_evapotranspiration = hourly.Variables(14).ValuesAsNumpy()
hourly_et0_fao_evapotranspiration = hourly.Variables(15).ValuesAsNumpy()
hourly_vapour_pressure_deficit = hourly.Variables(16).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(17).ValuesAsNumpy()
hourly_wind_speed_80m = hourly.Variables(18).ValuesAsNumpy()
hourly_wind_speed_120m = hourly.Variables(19).ValuesAsNumpy()
hourly_wind_speed_180m = hourly.Variables(20).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(21).ValuesAsNumpy()
hourly_wind_direction_80m = hourly.Variables(22).ValuesAsNumpy()
hourly_wind_direction_180m = hourly.Variables(23).ValuesAsNumpy()
hourly_wind_direction_120m = hourly.Variables(24).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(25).ValuesAsNumpy()
hourly_temperature_80m = hourly.Variables(26).ValuesAsNumpy()
hourly_temperature_120m = hourly.Variables(27).ValuesAsNumpy()
hourly_temperature_180m = hourly.Variables(28).ValuesAsNumpy()
hourly_soil_temperature_0cm = hourly.Variables(29).ValuesAsNumpy()
hourly_soil_temperature_6cm = hourly.Variables(30).ValuesAsNumpy()
hourly_soil_temperature_18cm = hourly.Variables(31).ValuesAsNumpy()
hourly_soil_temperature_54cm = hourly.Variables(32).ValuesAsNumpy()
hourly_soil_moisture_0_to_1cm = hourly.Variables(33).ValuesAsNumpy()
hourly_soil_moisture_1_to_3cm = hourly.Variables(34).ValuesAsNumpy()
hourly_soil_moisture_3_to_9cm = hourly.Variables(35).ValuesAsNumpy()
hourly_soil_moisture_9_to_27cm = hourly.Variables(36).ValuesAsNumpy()
hourly_soil_moisture_27_to_81cm = hourly.Variables(37).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["weather_code"] = hourly_weather_code
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["precipitation"] = hourly_precipitation
hourly_data["pressure_msl"] = hourly_pressure_msl
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["surface_pressure"] = hourly_surface_pressure
hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
hourly_data["visibility"] = hourly_visibility
hourly_data["evapotranspiration"] = hourly_evapotranspiration
hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["temperature_80m"] = hourly_temperature_80m
hourly_data["temperature_120m"] = hourly_temperature_120m
hourly_data["temperature_180m"] = hourly_temperature_180m
hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
hourly_data["soil_temperature_54cm"] = hourly_soil_temperature_54cm
hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
hourly_data["soil_moisture_1_to_3cm"] = hourly_soil_moisture_1_to_3cm
hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
hourly_data["soil_moisture_9_to_27cm"] = hourly_soil_moisture_9_to_27cm
hourly_data["soil_moisture_27_to_81cm"] = hourly_soil_moisture_27_to_81cm

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)

#hourly_dataframe.to_csv("buenos_aires_hourly_weather_2017_2020.csv", index=False)
hourly_dataframe.to_csv("./openMeteoProject/Data/quebec_hourly_weather_2023_2024.csv", index=False)

