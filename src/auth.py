import requests
import os
from log_helper import LogHelper

END_POINT = f'{os.getenv("END_POINT")}collections/users/auth-with-password'

class Auth:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Auth , cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.is_logged_in = False

    def ask(self):
        LogHelper.greeting()
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        print("IS_DEV" , LogHelper.is_dev_mode())
        if LogHelper.is_dev_mode():
            self.username = os.getenv("SIMPLE_USERNAME")
            self.password = os.getenv("SIMPLE_PASSWORD")
        self.login()
    
    def login(self) -> None:

        print("Logging in..." , END_POINT , self.username , self.password)
        try:
            response = requests.post(END_POINT , {
                "identity": self.username,
                "password": self.password
            })
            if response.status_code != 200:
                print(f"Error occurred while logging in: {response.json()['message']}")
                self.ask()
                return
            data = response.json()
            self.token = data["token"]
            self.record = data["record"]
            print('You have logged in...' , self.token)
        except Exception as e:
            print(f"Error occurred while fetching news: {e}")
        
    def logout(self) -> None:
        print("Logging out...")
        self.token = None