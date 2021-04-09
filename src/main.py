import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key = os.environ.get("OWM_API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "AC588afd4066e775e386de123e53db5c09"
auth_token = os.environ.get("AUTH_TOKEN")

weather_params={
    "lat": 28.538336, 
    "lon": -81.379234,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
sliced_data = (weather_data["hourly"][:12])

will_rain = False

for data in sliced_data:
    id_num = sliced_data[0]["weather"][0]["id"]
    if int(id_num) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
    .create(
         body='It is going to rain today, bring an umbrella.',
         from_='NUMBER TO SEND FROM',
         to='NUMBER TO RECIEVE'
     )

    print(message.status)
