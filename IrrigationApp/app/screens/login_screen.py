# app/screens/login_screen.py

from kivy.uix.screenmanager import Screen
from app.widgets.login_page import LoginPage

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginPage())
