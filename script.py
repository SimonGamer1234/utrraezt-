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
AD7 = os.getenv("REPO_VAR_7")
AD8 = os.getenv("REPO_VAR_8")
AD9 = os.getenv("REPO_VAR_9")
IDS = os.getenv("URLS")
TOKEN3 = os.getenv("TOKEN_SCRT_1")
BOT_TOKEN = f"Bot {os.getenv("BOT_TOKEN")}"
OWNER = "SimonGamer1234"
REPO = "aergaer"
GITHUB_TOKEN = os.getenv("GTOKEN")

author_ids = [1148657062599983237, 841925129323020298, 1285602869638070304, 1303383091468963841]
ids = IDS.split(',')
totalcount = 0
Ads = [AD1, AD2, AD3, AD4, AD5, AD6, AD7, AD8, AD9]
Ads2 = list(set(Ads))    
print(Ads)

def GetGuildIds(ids):
    GuildIds = []
    for ID in ids:
      header = {"Authorization": TOKEN3}
      response = requests.get(f"https://discord.com/api/v10/channels/{ID}", headers=header)
      if response.status_code == 200:
        data = response.json()
        guildId = int(data["guild_id"])
        GuildIds.append(guildId)
      else:
        print(f"Error with AdvertisingChannel Id: {ID} {response.status_code}")
    return GuildIds

def SearchForPosts(Keyword, ids, author_ids):
  print(ids)
  totalcount = 0
  header = {"Authorization": TOKEN3}
  params = {"content": Keyword, "author_id": author_ids, "limit": 25}
  for ID in ids:
    ID = int(ID)
    link = f"https://discord.com/api/v9/guilds/{ID}/messages/search"
    print(link)
    time.sleep(random.uniform(5,10))
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
  print(f"Total count: {totalcount} Ad: {Ad}")
  return totalcount

def UpdateVariable(Ad):
  Splitted1 = Ad.split("\n=divider=\n")
  Splitted2 = Ad.split("\r\n=divider=\r\n")
  if len(Splitted1) == 4:
    print(Splitted1)
    AdContent = Splitted1[0]
    TotalPosts = Splitted1[1]
    DaysLeft = Splitted1[2]
    KeyWords = Splitted1[3]
  elif len(Splitted2) == 4:
    print(Splitted2)
    AdContent = Splitted2[0]
    TotalPosts = Splitted2[1]
    DaysLeft = Splitted2[2]
    KeyWords = Splitted2[3]
  else:
     print("Error wiht splitting")
  print(Ad.split("\n=divider=\n"))
  if TotalPosts == "Base_Variable":
      print("Base Variable")
      return "Base_Variable", "Base_Variable", "Base_Variable", "Base_Variable"
  else:   
    NewDays = int(DaysLeft) - 1
    if NewDays == 0:
      SendMessage(f"Ad {AdContent} has expired", BOT_TOKEN, "https://discord.com/api/v9/channels/1302654558023057540/messages")
    NAME = f"AD_{Ads.index(Ad) + 1}"
    Text = f"{AdContent}\n=divider=\n{TotalPosts}\n=divider=\n{NewDays}\n=divider=\n{KeyWords}"
    headers = {
      'Accept': 'application/vnd.github+json',
      'Authorization': f'Bearer {GITHUB_TOKEN}',
      'X-GitHub-Api-Version': '2022-11-28',
      'Content-Type': 'application/json',}
    data = {"value": Text}
    response = requests.patch(f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{NAME}', headers=headers, json=data)
    print(response.status_code)
    return DaysLeft, TotalPosts, KeyWords, AdContent


def SendMessage(Message, Account, Destination):
  header = {"Authorization": Account}
  payload = {"content": Message}
  res = requests.post(Destination, data=payload, headers=header)
  print(f"Posted to {Destination} : {res.status_code}")  # Print response status


for Ad in Ads2:
  DaysLeft, SupposedPosts, KeyWords, AdContent = UpdateVariable(Ad)
  if SupposedPosts == "Base_Variable":
    continue
  else:
    GuildIds = GetGuildIds(ids)
    TotalPosts = SearchForPosts(KeyWords, GuildIds, author_ids)
    PostsLeft = int(SupposedPosts) - TotalPosts
    if PostsLeft > 0:
      SendMessage(f"Ad {Ad} \n\n Days left:  {DaysLeft} \n\n Posts left: {PostsLeft}", BOT_TOKEN, "https://discord.com/api/v9/channels/1302654558023057540/messages")
    else:
      SendMessage(f"Ad {Ad} can be removed \n\n {DaysLeft}  {PostsLeft}", BOT_TOKEN, "https://discord.com/api/v9/channels/1302654558023057540/messages")
