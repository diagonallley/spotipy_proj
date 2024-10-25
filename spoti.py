# import json
# import PIL
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.live import Live
from time import sleep
# import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# import pyperclip
# from io import BytesIO
from PIL import Image as PILImage
# import keyboard
import time
load_dotenv()


# Example: Get current playback information

def initialize():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-playback-state user-modify-playback-state user-read-recently-played",
        # SCOPE = 'user-modify-playback-state user-read-playback-state'

    ))
    return sp


sp = initialize()

# def download_img(url):
#     resp=requests.get(url)
#     img=PIL.Image.open(BytesIO(resp.content))
#     return img


def display_title():

    while True:
        global sp
        console = Console()
        current_playback = sp.current_playback()
        if current_playback is None:
            print("No song playing")
            inp = input(
                "DO you want to play previous song? Press y key to continue")
            if inp == "y":
                sp.start_playback()
                sp = sp.current_playback()

        # time.sleep(5)
        # pyperclip.copy(json.dumps(current_playback["is_playing"], indent=4))
        # pyperclip.copy(current_playback["item"]["album"]["images"][0]["url"])

        if (current_playback["is_playing"]):
            name = current_playback["item"]["name"]
            artists = current_playback["item"]["artists"][0]["name"]

            console.print(f"playing {name} by {artists}",
                          style="bold cyan", justify="center")
            time.sleep(5)

        else:
            console.print(
                f"Last played track => {current_playback['item']['name']} by {current_playback['item']['artists'][0]['name']}", style="cyan", justify="center")
            inp = console.input(
                "Press n for next, p for previous, space to play/pause")
            time.sleep(5)
            if (inp == "n"):
                sp.next_track()
            elif (inp == 'p'):
                sp.previous_track()
            elif (inp == 'h'):

                sp.start_playback()

def handle_playback():
    """
    Manages Spotify playback through console inputs.
    This function continuously checks the current playback status and allows the user to control playback
    through various console inputs. The user can play the previous song, resume playback, skip to the next 
    track, go to the previous track, pause/resume playback, shuffle the playlist, or quit the playback control.
    Console Inputs:
    - 'y': Play the previous song if no song is currently playing.
    - 'p': Resume playback if a song is paused.
    - 'N': Skip to the next track.
    - 'P': Go to the previous track.
    - 'H': Pause or resume playback.
    - 'sh': Shuffle the playlist.
    - 'q': Quit the playback control.
    The function uses the `Console` class from the `rich` library for styled console output and input prompts.
    """
    console=Console()
    global sp
    cont=True
    while cont:
        current_playback=sp.current_playback()
        if not current_playback:
            print("No song playing")
            inp=input("[bold cyan]Do you want to play previous song? Press y key to continue:[/bold cyan] ")
            # inp = console.input("[bold yellow]Do you want to play previous song? Press y key to continue:[/bold yellow] ")

            if inp=="y":
                sp.start_playback()
                sp=sp.current_playback()
                continue
            else:
                cont=False
                break
        else:
            if(sp.current_playback()['is_playing']):
                console.print(f"Playing {current_playback['item']['name']} by {current_playback['item']['artists'][0]['name']}", style="bold cyan", justify="center")
                console.print(f"Progress: {current_playback['progress_ms']/1000}/{current_playback['item']['duration_ms']/1000} seconds", style="bold cyan", justify="center")
            else:
                console.print(f"Last played track => {current_playback['item']['name']} by {current_playback['item']['artists'][0]['name']}", style="cyan", justify="center")
                inp=input("Press p to resume playback\n")
                if inp=="p":
                    sp.start_playback()
                    console.clear()
                    continue
            
            inp = console.input("[bold yellow]Press N for ⏭, P for ⏮, H to ⏯:[/bold yellow] ")
            inp=inp.lower()
            if inp=="n":
                sp.next_track()
                time.sleep(0.5)
                current_playback=sp.current_playback()
                console.clear()
                continue
            elif inp=="p":
                sp.previous_track()
                time.sleep(0.5)
                current_playback=sp.current_playback()
                console.clear()
                continue
            elif inp=="h":
                if sp.current_playback()['is_playing']:
                    sp.pause_playback()
                    console.clear()
                    continue
                sp.start_playback()
                time.sleep(0.5)
                current_playback=sp.current_playback()
                console.clear()
                continue
            elif input=="sh":
                sp.shuffle()
                console.clear()
                continue
            elif input=="q":
                break


# keyboard.is_pressed('space')
# display_title()
if __name__ == "__main__":
    handle_playback()


# manage playback


# resp["progress_ms"]
# resp["item"]["duration_ms"]