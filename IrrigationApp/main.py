# main.py

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from pymongo.errors import ConnectionFailure, ConfigurationError
from app.screens.empty_screen import EmptyScreen
from app.screens.login_screen import LoginScreen
from app.db.db_config import initialize_db

class IrrigationApp(MDApp):
    popup = None

    def build(self):
        self.sm = ScreenManager()
        # Add initial empty screen
        self.empty_screen = EmptyScreen(name='empty')
        self.sm.add_widget(self.empty_screen)
        # Attempt to check database connection
        self.check_database_connection()
        return self.sm

    def check_database_connection(self):
        try:
            # Initialize the database
            client, db, users_collection = initialize_db()
            # Test connection
            client.admin.command('ping')
            print("Successfully connected to the database.")
            
            # If connection is successful, switch to the login page
            self.login_screen = LoginScreen(name='login')
            self.sm.add_widget(self.login_screen)
            self.sm.current = 'login'
        except (ConnectionFailure, ConfigurationError) as e:
            # Handle connection failure and display an error popup
            print(f"Connection error: {str(e)}")
            self.show_error_popup("Unable to connect to the database. Please check your internet connection.")

    def show_error_popup(self, message):
        # Implementation for showing error popup
        pass

    def retry_connection(self, instance):
        self.close_popup()
        self.check_database_connection()

    def exit_app(self, instance):
        self.stop()

    def close_popup(self):
        if self.popup:
            self.popup.dismiss()
            self.popup = None

if __name__ == '__main__':
    IrrigationApp().run()
