import os

class LogHelper:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def greeting():
        print('----------------Welcome to MoodCMD!----------------')

    @staticmethod
    def heading(title : str):
        print(f'----------------{title}----------------')

    @staticmethod
    def menu():
        LogHelper.clear()
        LogHelper.heading("Select a Command to Run")
        print("1. Add Mood")
        print("2. Mood Board")
        print("3. Quit")