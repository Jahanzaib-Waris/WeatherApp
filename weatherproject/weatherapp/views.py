from django.shortcuts import render, HttpResponse
import requests
from datetime import datetime
from apiip import apiip

# Create your views here.

def home(request):

    api_client = apiip('Your API KEY')

    # ip = request.META.get('REMOTE_ADDR')
    info = api_client.get_location()
    loc = info['city']

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = loc
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    PARAMS = {
        'units': 'metric',
    }
    data = requests.get(url, PARAMS).json()
    forecasts = []
    def extract_date(datetime_str):
        # Parse the datetime string
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        # Extract and return the date part
        return dt.date().isoformat()
    
    added_dates = set()

    for forecast in data['list']:
        day = extract_date(forecast['dt_txt'])
        if day not in added_dates:
            forecasts.append({
                'day': day,
                'temp': forecast['main']['temp'],
                'highest_temp': forecast['main']['temp_max'],
                'lowest_temp': forecast['main']['temp_min'],
                'summary': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon'],
                'humidity': forecast['main']['humidity'],
                'wind': forecast['wind']['speed'],
                'pressure': forecast['main']['pressure'],
                'description': forecast['weather'][0]['main']
            })
            added_dates.add(day)

            if len(forecasts) == 5:
                break

    return render(request, 'weatherapp/index.html', {'city':city, 'forecast':forecasts})