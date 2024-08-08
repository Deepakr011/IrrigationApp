# app/widgets/underline_text_input.py

from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, RoundedRectangle

class UnderlineTextInput(TextInput):
    def __init__(self, **kwargs):
        super(UnderlineTextInput, self).__init__(**kwargs)
        self.background_normal = ''  # Remove default background
        self.background_active = ''  # Remove active background
        self.cursor_color = (0.2, 0.2, 0.2, 1)  # Dark gray cursor color
        self.foreground_color = (0.2, 0.2, 0.2, 1)  # Text color
        self.hint_text_color = (0.6, 0.6, 0.6, 1)  # Hint text color
        self.padding = [10, 10, 10, 10]  # Padding for all sides
        self.halign = 'left'  # Left alignment
        self.radius = [10]  # Radius for rounded corners
        self.bind(focus=self.update_graphics, size=self.update_graphics, pos=self.update_graphics)

    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
            Color(0.3, 0.3, 0.3, 1)  # Gray border
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1.5)
            Color(0.3, 0.3, 0.3, 1 if self.focus else 0.5)  # Darker underline when focused
            Line(points=[self.x + 10, self.y, self.right - 10, self.y], width=1.5)
