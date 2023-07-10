import requests
from dotenv import load_dotenv
import json
import time
import os
import numpy as np

load_dotenv()

RATE_LIMIT_DELAY = 0.67  # Delay in seconds between consecutive requests (1.5 requests per second)
MAX_REQUESTS = 90  # Maximum number of requests allowed per minute
API_ERR = []
ERR = []

# Load access token and refresh token from external file
access_token = os.getenv("ACCESS_TOKEN")

def add_to_json(json_obj, file):
    # Convert the JSON object to a string
    json_string = json.dumps(json_obj)
    # Open the file in append mode and write the JSON object
    with open(file, 'a') as file:
        file.write(json_string + '\n')
    
    print("Added to file.")

def fetch_user_anime_list(username):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Fetch user's anime list
    anime_url = f"https://api.myanimelist.net/v2/users/{username}/animelist?fields=list_status&limit=1000&type=anime"
    
    try:
        anime_response = requests.get(anime_url, headers=headers)
        if anime_response.status_code == 200:
            anime_data = anime_response.json()
            anime_ratings = [entry["list_status"]["score"] for entry in anime_data["data"]]
            # print("Anime Ratings:", anime_ratings)
            return {"user": username, "data": anime_data["data"]}
        else:
            ERR.append(username)
            print("Failed to fetch anime ratings.")
            print(anime_response.status_code)
    except requests.exceptions.RequestException as e:
        API_ERR.append(id)
        print("API Error:", e)

def fetch_user_manga_list(username):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Fetch user's manga list
    manga_url = f"https://api.myanimelist.net/v2/users/{username}/mangalist?fields=list_status&limit=1000&type=manga"

    try:
        manga_response = requests.get(manga_url, headers=headers)
        if manga_response.status_code == 200:
            manga_data = manga_response.json()
            manga_ratings = [entry["list_status"]["score"] for entry in manga_data["data"]]
            # print("Manga Ratings:", manga_ratings)
            return {"user": username, "data": manga_data["data"]}
        else:
            ERR.append(username)
            print("Failed to fetch manga ratings.")
    except requests.exceptions.RequestException as e:
        API_ERR.append(id)
        print("API Error:", e)

def process_user(username):
    print(f'fetching {username}')
    anime_list_status = fetch_user_anime_list(username)
    time.sleep(RATE_LIMIT_DELAY)  # Delay between consecutive requests
    manga_list_status = fetch_user_manga_list(username)
    time.sleep(RATE_LIMIT_DELAY)
    add_to_json(anime_list_status, 'user_anime.jsonl')
    add_to_json(manga_list_status, 'user_manga.jsonl')
    
# Example usage
# username = "Xinil"
# process_user(username)

# Load the JSON file
with open('batch_1.json', 'r') as file:
    batch_data = json.load(file)
for index, username in enumerate(batch_data['usernames'],1):
    process_user(username)
    print(f"Processed {index} usernames")

print(f'Errors: {ERR}, {API_ERR}')
np.savez("UMerr.npz", array1=np.array(ERR), array2=np.array(API_ERR))
print("Data fetching completed.")
