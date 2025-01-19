import requests
import time
import random
import sys
import os

# Parse input arguments
urls_string = sys.argv[3]  # Repository variable containing URLs as a string
token = sys.argv[2]        # Authorization token
advertisement = sys.argv[1]  # Advertisement content
tracker_file = "ad_tracker.txt"

# Split URLs string into a list of URLs
urls = [url.strip() for url in urls_string.split(",")]

# Ensure tracker file exists
if not os.path.exists(tracker_file):
    with open(tracker_file, "w") as file:
        file.write("0")  # Initialize with 0

# Load the current ad number
with open(tracker_file, "r") as file:
    current_ad = int(file.read().strip())

# Post the ad
delay = random.uniform(2, 5)  # Random delay between posts
try:
    for url in urls:
        response = requests.post(url, data={"content": advertisement}, headers={"Authorization": token})
        if response.status_code == 200:
            print(f"Successfully posted to {url}")
        else:
            print(f"Failed to post to {url}: {response.status_code} - {response.text}")
        time.sleep(delay)

    # Update the tracker file with the next ad number
    with open(tracker_file, "w") as file:
        file.write(str((current_ad + 1) % 6))  # Assuming 6 ads in total
except Exception as e:
    print(f"Error posting to URLs: {e}")
