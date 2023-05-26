from fastapi import FastAPI
import requests
import os

app = FastAPI()

TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_AUTH_TOKEN = os.environ.get("TWITCH_AUTH_TOKEN")

headers = { 
    "Client-ID": TWITCH_CLIENT_ID,
    "Authorization": "Bearer " + TWITCH_AUTH_TOKEN,
    "Accept": "application/vnd.twitchtv.v5+json"
    }

@app.get("/get-game")
def get_game():
    url = "https://api.twitch.tv/helix/games"
    params = {
            "name": "Black Desert"
            }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "fail to fetch games",
            "resp": response.json()
            }
    

@app.get("/top-streams")
def get_top_streams():
    url = "https://api.twitch.tv/helix/streams"
    params = {
            "game": "League of Legends",
            "first": 10 # default 20
            }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "Failed to fetch top streams",
            "resp": response.json()
            }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

