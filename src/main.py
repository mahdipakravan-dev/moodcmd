from auth import Auth
from log_helper import LogHelper
from commands.invoker import CommandInvoker
from commands.cmd_add_mood import AddMood
from commands.cmd_mood_board import MoodBoard
from dotenv import load_dotenv

load_dotenv()

def main():
    Auth().ask()
    invoker = CommandInvoker()

    invoker.add_command("1",AddMood())
    invoker.add_command("2",MoodBoard())

    while True:
        LogHelper.menu()
        choice = input("Enter your choice : ")

        if choice == 'quit':
            print('Exiting...')
            break
        invoker.execute_command(choice)

if __name__ == '__main__':
    main()