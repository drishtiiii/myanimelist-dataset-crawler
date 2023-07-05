import requests
import os
from dotenv import load_dotenv
import json
import time
import csv
import numpy as np

load_dotenv()

RATE_LIMIT_DELAY = 0.67  # Delay in seconds between consecutive requests (1.5 requests per second)
MAX_REQUESTS = 90  # Maximum number of requests allowed per minute
API_ERR = []
ERR = []

def add_to_json(json_obj, file):
    # Convert the JSON object to a string
    json_string = json.dumps(json_obj)
    # Open the file in append mode and write the JSON object
    with open(file, 'a') as file:
        file.write(json_string + '\n')
    
    print("Added to file.")

def refresh_access_token(refresh_token, client_id, client_secret):
    url = "https://myanimelist.net/v1/oauth2/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]
        print("Access Token Refreshed!")
        return access_token, refresh_token
    except requests.exceptions.RequestException as e:
        print("Token Refresh Error:", e)

# Load client ID and client secret from .env file
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Load access token and refresh token from external file
# with open("tokens.txt", "r") as file:
#     tokens = file.readlines()
#     access_token = tokens[0].strip()
#     refresh_token = tokens[1].strip()
access_token = os.getenv("ACCESS_TOKEN")
refresh_token = os.getenv("REFRESH_TOKEN")

def fetch_anime_data(id):
    anime_id = id
    fields = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields={fields}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.raise_for_status()
            anime_data = response.json()
            # print("Anime Data:", anime_data)
            # json_data = json.dumps(anime_data, indent=4)
            return anime_data
        else:
            ERR.append(id)
            print("Error fetching anime data")
            print(response.status_code)
    except requests.exceptions.RequestException as e:
        API_ERR.append(id)
        print("API Error:", e)

def fetch_manga_data(id):
    manga_id = id
    fields = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_volumes,num_chapters,authors{first_name,last_name},pictures,background,related_anime,related_manga,recommendations,serialization"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"https://api.myanimelist.net/v2/manga/{manga_id}?fields={fields}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.raise_for_status()
            anime_data = response.json()
            # print("Anime Data:", anime_data)
            # json_data = json.dumps(anime_data, indent=4)
            return anime_data
        else:
            ERR.append(id)
            print("Error fetching manga data")
            print(response.status_code)
    except requests.exceptions.RequestException as e:
        API_ERR.append(id)
        print("API Error:", e)

# fetch_anime_data(1)

# Check if access token expired
# If expired, refresh the access token
# Update the access token and refresh token with the refreshed values
# if access_token_expired:
#     access_token, refresh_token = refresh_access_token(refresh_token, client_id, client_secret)

# Fetch anime data for IDs 1 to 50,000
animelist_range = (1, 10000)
mangalist_range = (1, 30000)

for manga_id in range(mangalist_range[0], mangalist_range[1]):
    print(f'Fetching manga with id {manga_id} ')
    manga_data = fetch_manga_data(manga_id)
    file = f'mangalist_{mangalist_range[0]}_{mangalist_range[1]}.jsonl'
    if manga_data:
        # saves into csv
        add_to_json(manga_data, file)
        
    time.sleep(RATE_LIMIT_DELAY)  # Delay between consecutive requests


print(f'Errors: {ERR}, {API_ERR}')
np.savez("Merr.npz", array1=np.array(ERR), array2=np.array(API_ERR))
print("Manga data fetching completed.")
