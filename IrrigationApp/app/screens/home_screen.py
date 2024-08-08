# app/screens/home_screen.py

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle

class HomePage(BoxLayout):
    def __init__(self, user_email, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 40, 20, 40]
        self.spacing = 20

        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray background color
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

        self.user_email = user_email

        welcome_label = MDLabel(
            text=f'Welcome, {self.user_email}',
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint=(1, 0.1)
        )

        self.add_widget(welcome_label)

        # Additional widgets and layout for the home page can be added here
