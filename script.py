import os
import random
import requests
import time
import json

# Retrieve the environment variables
AD1 = os.getenv("REPO_VAR_1")
AD2 = os.getenv("REPO_VAR_2")
AD3 = os.getenv("REPO_VAR_3")
AD4 = os.getenv("REPO_VAR_4")
AD5 = os.getenv("REPO_VAR_5")
AD6 = os.getenv("REPO_VAR_6")
IDS = os.getenv("URLS")
TOKEN1 = os.getenv("TOKEN_SCRT_1")
BOT_TOKEN = os.getenv("BOT_TOKEN")

author_ids = [1148657062599983237, 841925129323020298, 1285602869638070304, 1303383091468963841]
ids = IDS.split(',')
totalcount = 0
Ads = [AD1, AD2, AD3, AD4, AD5, AD6, AD7, AD8, AD9, AD10, AD11, AD12]
for Ad in Ads:
  for Ad2 in Ads:
    if Ad == Ad2:
      Ads.remove(Ad2)
    
print(Ads)
for Ad in Ads:
  totalcount = 0
  header = {"Authorization": TOKEN1}   
  params = {"content": Ad, "author_id":author_ids, "limit": 25}
  for ID in ids:
    response = requests.get(f"https://discord.com/api/v10/channels/{ID}", headers=header)
    data = response.json()
    server_id = data['guild_id']
    intID = int(server_id)
    link = f"https://discord.com/api/v9/guilds/{intID}/messages/search"
    print(link)
    time.sleep(random.uniform(2,3))
    res = requests.get(link, params=params, headers=header)
    if res.status_code == 200:
        try:
            data = res.json()
            total_results = data.get("total_results", 0)
            totalcount += int(total_results)
            print(total_results)  # Parsed JSON response
        except requests.exceptions.JSONDecodeError:
            print("Response is not JSON. Raw response:")
            print(res.text)
    else:
        print(f"Request failed with status code {res.status_code}: {res.text}")
  print(totalcount)
  botheader = {"Authorization": f"Bot {BOT_TOKEN}"}
  CONTENT = f"Avertisement\n{Ad}\n\n{totalcount}"
  payload = {"content": CONTENT}
  LINK = "https://discord.com/api/v9/channels/1302654581758496809/messages"
  post = requests.post(LINK, data=payload, headers=botheader)
  print(post.text)
