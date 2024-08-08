# app/widgets/login_page.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
import uuid
import os
from pymongo.errors import ConnectionFailure, ConfigurationError, DuplicateKeyError
from bcrypt import hashpw, gensalt, checkpw
import socket
from pymongo import MongoClient
from pymongo import MongoClient
from app.widgets.underline_text_input import UnderlineTextInput
from app.screens.home_screen import HomePage
from app.db.db_config import initialize_db

# MongoDB setup
client = None
db = None
users_collection = None

def initialize_db():
    global client, db, users_collection
    try:
        client = MongoClient(
            "mongodb+srv://deepak:Deepakr123@cluster0.vh0c9g2.mongodb.net/?retryWrites=true&w=majority",
            serverSelectionTimeoutMS=5000  # 5-second timeout
        )
        db = client['IrrigationApp']
        users_collection = db['users']
        # Test connection
        client.admin.command('ping')
    except (ConnectionFailure, ConfigurationError) as e:
        client = None
        db = None
        users_collection = None
        print(f"Failed to connect to MongoDB: {str(e)}")

initialize_db()

class LoginPage(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [40, 80, 40, 80]  # Adjusted padding for better layout
        self.spacing = 20

        # Check if the device is already registered
        if self.check_device_registration():
            self.redirect_to_home(self.get_device_email())
        else:
            self.add_widget(Label(
                text='Login to Irrigation App',
                font_size='24sp',
                bold=True,
                size_hint=(1, 0.2),
                color=(0.1, 0.3, 0.7, 1),  # Blue text color
                halign='center'
            ))

            self.username_input = UnderlineTextInput(
                hint_text='Email',
                size_hint=(1, 0.1),
                multiline=False
            )
            self.add_widget(self.username_input)

            # Create a layout for the password input and the eye icon inside it
            password_layout = RelativeLayout(size_hint=(1, 0.1))

            self.password_input = UnderlineTextInput(
                hint_text='Password',
                password=True,
                multiline=False
            )
            password_layout.add_widget(self.password_input)

            eye_button = MDIconButton(
                icon='eye',
                size_hint=(None, None),
                size=(30, 30),  # Small button size
                pos_hint={'right': 1, 'center_y': 0.5},  # Position inside the text input
                md_bg_color=(0, 0, 0, 0),  # Transparent background
                theme_text_color='Custom',
                text_color=(0.1, 0.6, 0.8, 1)  # Custom color (e.g., cyan)
            )
            eye_button.bind(on_press=self.toggle_password_visibility)
            password_layout.add_widget(eye_button)

            self.add_widget(password_layout)

            button_layout = BoxLayout(size_hint=(1, 0.2), spacing=20)

            # Login Button with Label below
            login_button_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 1), spacing=10, padding=[20, 0, 0, 0])
            login_button = MDIconButton(
                icon='login',
                size_hint=(None, None),
                size=(60, 60),  # Small round button size
                md_bg_color=(0.1, 0.5, 0.9, 1),  # Blue background
                theme_text_color='Custom',
                text_color=(1, 0, 0, 1)  # Red icon color
            )
            login_button.bind(on_press=self.validate_credentials)
            login_label = MDLabel(
                text='Login',
                halign='center',
                size_hint=(None, None),
                size=(60, 50),
                theme_text_color='Primary'
            )
            login_button_box.add_widget(login_button)
            login_button_box.add_widget(login_label)
            button_layout.add_widget(login_button_box)

            # Register Button with Label below
            register_button_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 1), spacing=10, padding=[20, 0, 0, 0])
            register_button = MDIconButton(
                icon='account-plus',
                size_hint=(None, None),
                size=(60, 60),  # Small round button size
                md_bg_color=(0.2, 0.7, 0.2, 1),  # Green background
                theme_text_color='Custom',
                text_color=(0, 0, 1, 1)  # Blue icon color
            )
            register_button.bind(on_press=self.show_registration_popup)
            register_label = MDLabel(
                text='Register',
                halign='center',
                size_hint=(None, None),
                size=(80, 50),
                theme_text_color='Primary'
            )
            register_button_box.add_widget(register_button)
            register_button_box.add_widget(register_label)
            button_layout.add_widget(register_button_box)

            self.add_widget(button_layout)

    def toggle_password_visibility(self, instance):
        self.password_input.password = not self.password_input.password

    def validate_credentials(self, instance):
        if not self.check_network():
            self.show_popup("Network Error", "No internet connection. Please check your network and try again.")
            return

        email = self.username_input.text
        password = self.password_input.text

        try:
            if client is None:
                initialize_db()  # Try to reconnect

            if client is None:
                raise ConnectionFailure("No connection to MongoDB.")

            user = users_collection.find_one({"email": email})
            if user and checkpw(password.encode('utf-8'), user['password']):
                self.save_device_id(user["_id"])
                self.redirect_to_home(email)
            else:
                self.show_popup("Login Failed", "Invalid email or password. Please try again.")
        except (ConnectionFailure, ConfigurationError) as e:
            self.show_popup("Connection Error", f"Could not connect to the server: {str(e)}", retry=True)
        except Exception as e:
            self.show_popup("Error", f"An unexpected error occurred: {str(e)}")

    def check_network(self):
        try:
            # Check if the device can connect to a known site (e.g., Google)
            socket.create_connection(("www.google.com", 80), timeout=2)
            return True
        except OSError:
            return False

    def check_device_registration(self):
        if client is None:
            return False

        device_id = self.get_device_id()
        if device_id:
            return bool(users_collection.find_one({"device_id": device_id}))
        return False

    def get_device_email(self):
        device_id = self.get_device_id()
        if device_id:
            user = users_collection.find_one({"device_id": device_id})
            if user:
                return user.get("email")
        return ""

    def save_device_id(self, user_id):
        device_id = str(uuid.uuid4())
        device_id_path = "device_id.txt"

        # Save device_id locally
        with open(device_id_path, "w") as f:
            f.write(device_id)

        # Update device_id in MongoDB
        try:
            if client is None:
                initialize_db()  # Try to reconnect

            if client is None:
                raise ConnectionFailure("No connection to MongoDB.")

            users_collection.update_one({"_id": user_id}, {"$set": {"device_id": device_id}})
        except (ConnectionFailure, ConfigurationError) as e:
            self.show_popup("Connection Error", f"Could not update device ID: {str(e)}", retry=True)
        except Exception as e:
            self.show_popup("Error", f"An unexpected error occurred: {str(e)}")

    def get_device_id(self):
        device_id_path = "device_id.txt"
        if os.path.exists(device_id_path):
            with open(device_id_path, "r") as f:
                return f.read().strip()
        return None

    def redirect_to_home(self, email):
        self.clear_widgets()
        home_page = HomePage(user_email=email)
        self.add_widget(home_page)

    def show_registration_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=20, padding=[40, 20, 40, 20])
        popup_layout.add_widget(Label(text='Enter your registration details', font_size='18sp', bold=True, size_hint=(1, 0.2)))

        self.reg_email_input = UnderlineTextInput(hint_text='Email', size_hint=(1, 0.1), multiline=False)
        self.reg_password_input = UnderlineTextInput(hint_text='Password', password=True, size_hint=(1, 0.1), multiline=False)
        self.reg_confirm_password_input = UnderlineTextInput(hint_text='Confirm Password', password=True, size_hint=(1, 0.1), multiline=False)

        popup_layout.add_widget(self.reg_email_input)
        popup_layout.add_widget(self.reg_password_input)
        popup_layout.add_widget(self.reg_confirm_password_input)

        register_button = MDIconButton(
            icon='account-plus',
            size_hint=(None, None),
            size=(60, 60),
            md_bg_color=(0.2, 0.7, 0.2, 1)
        )
        register_button.bind(on_press=self.register_user)

        popup_layout.add_widget(register_button)

        self.registration_popup = Popup(title='Register', content=popup_layout, size_hint=(0.9, 0.6), auto_dismiss=True)
        self.registration_popup.open()

    def register_user(self, instance):
        email = self.reg_email_input.text
        password = self.reg_password_input.text
        confirm_password = self.reg_confirm_password_input.text

        if not self.check_network():
            self.show_popup("Network Error", "No internet connection. Please check your network and try again.")
            return

        if password != confirm_password:
            self.show_popup("Registration Failed", "Passwords do not match. Please try again.")
            return

        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        try:
            if client is None:
                initialize_db()  # Try to reconnect

            if client is None:
                raise ConnectionFailure("No connection to MongoDB.")

            users_collection.insert_one({"email": email, "password": hashed_password})
            self.show_popup("Success", "Registration successful. Please log in.")
            self.registration_popup.dismiss()
        except DuplicateKeyError:
            self.show_popup("Registration Failed", "Email is already registered. Please log in.")
        except (ConnectionFailure, ConfigurationError) as e:
            self.show_popup("Connection Error", f"Could not connect to the server: {str(e)}", retry=True)
        except Exception as e:
            self.show_popup("Error", f"An unexpected error occurred: {str(e)}")

    def show_popup(self, title, message, retry=False):
        popup_layout = BoxLayout(orientation='vertical', spacing=20, padding=[40, 20, 40, 20])
        popup_layout.add_widget(Label(text=message, size_hint=(1, 0.8)))
        
        if retry:
            retry_button = MDIconButton(
                icon='reload',
                size_hint=(None, None),
                size=(60, 60),
                md_bg_color=(0.8, 0.3, 0.3, 1),  # Red background for retry
                theme_text_color='Custom',
                text_color=(1, 1, 1, 1)  # White text color
            )
            retry_button.bind(on_press=self.retry_connection)
            popup_layout.add_widget(retry_button)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4), auto_dismiss=True)
        popup.open()

    def retry_connection(self, instance):
        initialize_db()
        if client is not None:
            self.clear_widgets()
            self.add_widget(LoginPage())
        else:
            self.show_popup("Connection Error", "Could not reconnect to the server. Please try again later.", retry=True)
