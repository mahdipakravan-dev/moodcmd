from commands.parent import Command
import datetime
import os
import requests
from log_helper import LogHelper
from auth import Auth

MOOD_API_URL = f'{os.getenv("END_POINT")}collections/moods/records'

class MoodBoard(Command):
    def __init__(self):
        pass

    @staticmethod
    def format_time(time: datetime.datetime):
        return time.strftime("%Y-%m-%d")

    def execute(self):
        LogHelper.clear()
        LogHelper.heading("List of Available DateTime Mood:")

        now = datetime.datetime.now()
        last_10_days = [now - datetime.timedelta(days=i) for i in range(10)]

        for i, day in enumerate(last_10_days, 1):
            print(f'{day.strftime("%Y-%m-%d")} ({i})')

        selected_date = input('\nSelect 1 of Dates: ')

        # Ensure valid date selection
        if not selected_date.isdigit() or not (1 <= int(selected_date) <= 10):
            print("Invalid selection! Please enter a number between 1 and 10.")
            return

        selected_datetime = last_10_days[int(selected_date) - 1].strftime("%Y-%m-%d")

        token = Auth().token
        if not token:
            print("You are not logged in! Please log in first.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        url = f"{MOOD_API_URL}?filter=(created~'{selected_datetime}')"

        print(f"\n🔄 Please wait... Fetching mood chart for {selected_datetime}...")

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if response.status_code not in (200, 201):
                print(f"❌ Failed to load mood: {data}")
                return

            LogHelper.clear()
            LogHelper.heading(f"{selected_datetime} Moods")

            mood_dict = {
                "Very Bad": 0,
                "Bad": 0,
                "Poker": 0,
                "Good": 0,
                "Very Good": 0
            }

            mood_mapping = {
                "1": "Very Bad",
                "2": "Bad",
                "3": "Poker",
                "4": "Good",
                "5": "Very Good"
            }

            for mood in data.get("items", []):
                mood_name = mood_mapping.get(mood.get("mood"))
                if mood_name:
                    mood_dict[mood_name] += 1

            for mood, count in mood_dict.items():
                print(f"{mood}: {count}")

        except requests.RequestException as e:
            print(f"❌ An error occurred: {e}")

        input("Press Enter to return to the menu...")
