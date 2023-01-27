import json
import requests
import os
import pandas as pd
import numpy as np

api_key = st.secrets["api_key"]

def get_details(place, travel_destination):
    # Get latitude and longitude of travel destination to ensure search results 
    # are biased towards the location of choice and not IP address
    assert type(travel_destination) == str, print(travel_destination,type(travel_destination))
    # Get Lat Lon of Travel Destination
    input = travel_destination
    formatted_input = input.replace(' ', '%20')
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key={}".format(formatted_input,api_key)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    _json = response.json()
    # Lat, Lon format
    destination_lat_lon = list(_json['candidates'][0]['geometry']['location'].values())
    
    # Get search result data
    assert type(place) == str
    input = place
    formatted_input = input.replace(' ', '%20')
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&Place=user_ratings_total%2Copening_hours%2Cprice_level&PlaceOpeningHours=weekday_text%2Cperiods&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&PlaceReview=rating&locationbias=circle%3A2000%40{}%2C{}&key={}".format(formatted_input,destination_lat_lon[0],destination_lat_lon[1],api_key)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    _json = response.json()
    try:
        address = _json['candidates'][0]['formatted_address']
        lon = _json['candidates'][0]['geometry']['location']['lat']
        lat = _json['candidates'][0]['geometry']['location']['lng']
        name = _json['candidates'][0]['name']
        rating = _json['candidates'][0]['rating']
    except Exception as e:
        rating = 0
    return _json, address, lon, lat, name, rating
