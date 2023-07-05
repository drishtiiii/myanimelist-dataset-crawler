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

# Load client ID and client secret from .env file
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Load access token and refresh token from external file
with open("tokens.txt", "r") as file:
    tokens = file.readlines()
    access_token = tokens[0].strip()
    refresh_token = tokens[1].strip()



headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

# Set the parameters for the request
limit = 500  # Number of anime per page
offset = 0  # Starting index
fields =  "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_volumes,num_chapters,authors{first_name,last_name},pictures,background,related_anime,related_manga,recommendations,serialization"

url = f"https://api.myanimelist.net/v2/manga/ranking?limit={limit}&fields={fields}&offset={offset}"

all_manga = []

# Make consecutive requests until all anime are fetched
while True:
    # Make the API request
    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Add the anime from the current page to the list
        all_manga.extend(data["data"])

        # Check if there are more pages to fetch
        if "paging" in data and "next" in data["paging"]:
            # Update the offset for the next page
            offset += limit
            print(f'page offset {offset}')
        else:
            # All anime have been fetched
            break
    else:
        print(f"Failed to retrieve manga. {response} {url}")

csv_file = 'manga_data.csv'

# Extract field names from the first anime
field_names = list(all_manga[0].keys())

# Open CSV file in write mode
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)

    writer.writeheader()  # Write header row

    # Write each anime as a row in the CSV file
    for manga in all_manga:
        writer.writerow(manga)

print('Manga data saved to CSV file:', csv_file)

# Print the total count of anime fetched
total_manga_count = len(all_manga)
print(f"Total anime count: {total_manga_count}")
