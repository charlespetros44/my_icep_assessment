import requests
from datetime import datetime, timedelta
import csv

def get_nws_forecast(gridpoints_url):
    response = requests.get(gridpoints_url)
    data = response.json()

    if response.status_code == 200:
        return data['properties']['periods']
    else:
        print(f"Error: {data['title']}")
        return None

# Example NWS API endpoint for San Francisco
nws_gridpoints_url = "https://api.weather.gov/gridpoints/MTR/84,105/forecast"

forecast_data = get_nws_forecast(nws_gridpoints_url)

if forecast_data:
    print("Weather Forecast for the Next Three Days:")
    for period in forecast_data[:3]:  # Only showing the first three periods
        start_time = datetime.fromisoformat(period['startTime'])
        end_time = datetime.fromisoformat(period['endTime'])
        temperature = period['temperature']
        precipitation = period.get('shortForecast', 'No precipitation forecasted')

        print(f"{start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')}: "
              f"Temperature: {temperature}°F, Forecast: {precipitation}")

    # Save the forecast data to a CSV file
    csv_file_path = "weather_forecast.csv"
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['Start Time', 'End Time', 'Temperature (°F)', 'Forecast']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for period in forecast_data[:3]:
            start_time = datetime.fromisoformat(period['startTime']).strftime('%Y-%m-%d %H:%M')
            end_time = datetime.fromisoformat(period['endTime']).strftime('%Y-%m-%d %H:%M')
            temperature = period['temperature']
            precipitation = period.get('shortForecast', 'No precipitation forecasted')

            writer.writerow({
                'Start Time': start_time,
                'End Time': end_time,
                'Temperature (°F)': temperature,
                'Forecast': precipitation
            })

    print(f"Forecast data saved to: {csv_file_path}")
else:
    print("Failed to retrieve weather forecast.")
