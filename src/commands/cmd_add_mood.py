from commands.parent import Command
from log_helper import LogHelper
from auth import Auth
import requests
import os

MOOD_API_URL = f'{os.getenv("END_POINT")}collections/moods/records'

class AddMood(Command):
    def __init__(self):
        pass
        
    def execute(self):
        LogHelper.clear()
        LogHelper.heading("What's Your Current Mood ?")
        print('1. Very Happy')
        print('2. Happy')
        print('3. Poker')
        print('4. Bad')
        print('5. Very Bad')
        mood = input('\n Select your Current Mood (1-5) : ')

        token = Auth().token
        user = Auth().record
        if not token:
            print("You are not logged in! Please log in first.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {
            "mood": mood,
            "user" : user["id"]
        }

        print(f"Adding Mood '{mood}' with Token...")

        try:
            response = requests.post(MOOD_API_URL, json=data, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                print("Mood successfully added!")
            else:
                print(f"Failed to add mood: {response.json()}")
        except Exception as e:
            print(f"An error occurred: {e}")