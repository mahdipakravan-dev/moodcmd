from commands.parent import Command
import datetime
from log_helper import LogHelper
from auth import Auth
import requests
import os

MOOD_API_URL = f'{os.getenv("END_POINT")}collections/moods/records'

class MoodBoard(Command):
    def __init__(self):
        pass
        
    def formatTime(time : datetime):
        return time.strftime("%Y_%m_%d")
    def execute(self):
        LogHelper.clear()
        LogHelper.heading("List of Available DateTime Mood:")
        now = datetime.datetime.now();
        last10Days = [now - datetime.timedelta(i) for i in range(0,10)]
        for i,day in enumerate(last10Days):
            print(f'{day} ({i + 1})')
        
        selectedDate = input('\nSelect 1 of Dates : ')

        token = Auth().token
        user = Auth().record
        if not token:
            print("You are not logged in! Please log in first.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        selectedDateTime = last10Days[int(selectedDate) - 1].strftime("%Y-%m-%d")
        URL = MOOD_API_URL + f"?filter=(created~'{selectedDateTime}')"

        print(f"\n \nPlease Wait...")
        print(f'We are looking for your mood chart in {selectedDateTime}...')

        try:
            response = requests.get(URL, headers=headers)
            data = response.json()            
            if response.status_code == 200 or response.status_code == 201:
                LogHelper.clear()
                LogHelper.heading(f"{selectedDateTime} Moods")
                mood_dict = {
                    "VeryBad" : 0,
                    "Bad" : 0,
                    "Poker" : 0,
                    "Good" : 0,
                    "VeryGood" : 0
                }
                for mood in data["items"]:
                    if mood["mood"] == '1':
                        mood_dict["VeryBad"] += 1
                    if mood["mood"] == '2':
                        mood_dict["Bad"] += 1
                    if mood["mood"] == '3':
                        mood_dict["Poker"] += 1
                    if mood["mood"] == '4':
                        mood_dict["Good"] += 1
                    if mood["mood"] == '5':
                        mood_dict["VeryGood"] += 1

                for mood in mood_dict.keys():
                    print(f'{mood} : {mood_dict[mood]}')
            else:
                print(f"Failed to Load mood: {response.json()}")
            input("Press Enter to Back to Menu...")
        except Exception as e:
            print(f"An error occurred: {e}")

        input()