import pandas as pd
from datetime import datetime
import requests_cache
import openmeteo_requests
from retry_requests import retry
from zoneinfo import ZoneInfo

# Setup client
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Get today's date in Eastern Time
today_eastern = datetime.now(ZoneInfo("America/Toronto")).date()
start_date = today_eastern.isoformat()
end_date = today_eastern.isoformat()

# API parameters (Quebec example)
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": [
        "temperature_2m", "weather_code", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
        "precipitation", "pressure_msl", "cloud_cover", "surface_pressure", "cloud_cover_low",
        "cloud_cover_mid", "cloud_cover_high", "visibility", "et0_fao_evapotranspiration",
        "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m",
        "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_gusts_10m",
        "temperature_80m", "temperature_120m"
    ],
    "timezone": "UTC",
    "start_date": start_date,
    "end_date": end_date
}

# Request and parse response
response = openmeteo.weather_api(url, params=params)[0]
hourly = response.Hourly()

# Extract date and data
dates = pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
)

data = {
    "date": dates,
    "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
    "weather_code": hourly.Variables(1).ValuesAsNumpy(),
    "relative_humidity_2m": hourly.Variables(2).ValuesAsNumpy(),
    "dew_point_2m": hourly.Variables(3).ValuesAsNumpy(),
    "apparent_temperature": hourly.Variables(4).ValuesAsNumpy(),
    "precipitation": hourly.Variables(5).ValuesAsNumpy(),
    "pressure_msl": hourly.Variables(6).ValuesAsNumpy(),
    "cloud_cover": hourly.Variables(7).ValuesAsNumpy(),
    "surface_pressure": hourly.Variables(8).ValuesAsNumpy(),
    "cloud_cover_low": hourly.Variables(9).ValuesAsNumpy(),
    "cloud_cover_mid": hourly.Variables(10).ValuesAsNumpy(),
    "cloud_cover_high": hourly.Variables(11).ValuesAsNumpy(),
    "visibility": hourly.Variables(12).ValuesAsNumpy(),
    "et0_fao_evapotranspiration": hourly.Variables(13).ValuesAsNumpy(),
    "vapour_pressure_deficit": hourly.Variables(14).ValuesAsNumpy(),
    "wind_speed_10m": hourly.Variables(15).ValuesAsNumpy(),
    "wind_speed_80m": hourly.Variables(16).ValuesAsNumpy(),
    "wind_speed_120m": hourly.Variables(17).ValuesAsNumpy(),
    "wind_direction_10m": hourly.Variables(18).ValuesAsNumpy(),
    "wind_direction_80m": hourly.Variables(19).ValuesAsNumpy(),
    "wind_direction_120m": hourly.Variables(20).ValuesAsNumpy(),
    "wind_gusts_10m": hourly.Variables(21).ValuesAsNumpy(),
    "temperature_80m": hourly.Variables(22).ValuesAsNumpy(),
    "temperature_120m": hourly.Variables(23).ValuesAsNumpy(),
}


df_today = pd.DataFrame(data)

df_today["date"] = df_today["date"].dt.tz_convert("America/Toronto")

eastern_now = datetime.now(ZoneInfo("America/Toronto")).replace(minute=0, second=0, microsecond=0)
print("Hora actual (America/Toronto):", eastern_now)

last_row = df_today[df_today["date"] == eastern_now].copy()

# Save as CSV
last_row.to_csv("./openMeteoProject/Data/quebec_current_weather.csv", index=False)
