from commands.parent import Command
from log_helper import LogHelper
from auth import Auth
from services import Services
import os

MOOD_API_URL = f'{os.getenv("END_POINT")}collections/moods/records'

class AddMood(Command):
    def __init__(self, auth_instance=None):
        self.auth = auth_instance if auth_instance else Auth()
        self.services = Services(self.auth)

    def execute(self):
        LogHelper.clear()
        LogHelper.heading("What's Your Current Mood ?")
        print('1. Very Happy')
        print('2. Happy')
        print('3. Poker')
        print('4. Bad')
        print('5. Very Bad')
        mood = input('\nSelect your Current Mood (1-5) : ')

        user = self.auth.record

        data = {
            "mood": mood,
            "user": user["id"]
        }

        print(f"\n \nPlease Wait...")

        response = self.services.post(MOOD_API_URL, data=data)

        if response is not None:
            if isinstance(response, dict) and ('id' in response):
                print("Mood successfully added!")
            elif isinstance(response, int) and 200 <= response < 300:
                print("Mood successfully added!")
            else:
                print(f"Failed to add mood.")
                if isinstance(response, dict):
                    print(f"Details: {response}")
                elif isinstance(response, int):
                    print(f"Status Code: {response}")
            input("Press Enter to Back to Menu...")