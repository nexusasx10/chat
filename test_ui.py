import re
from tkinter import Tk, Canvas, Frame, Text


class Interface:
    def __init__(self, width, height, title):
        self.tk = Tk()
        self.tk.title(title)
        self.tk.geometry(f'{width}x{height}')
        self.canvas = Canvas(width=0, bg='#F9EFDD', height=0, highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)
        self.messages = []

        self.text_field = Frame(bg='white')
        self.text_field.pack(fill='x')
        self.entry = Text(self.text_field, bd=0, font='Consolas 11')
        self.entry.pack(padx=10, pady=10, fill='x', expand=1)
        self.entry.focus()

        self.entry.bind('<KeyRelease>', self.entry_size_control)
        self.entry.bind('<KeyPress>', self.entry_size_control)
        self.entry.bind('<Configure>', self.entry_size_control)
        self.tk.bind('<KeyPress>', self.on_key_press)
        self.tk.bind('<KeyRelease>', self.on_key_release)

        self.send = True

    def on_key_press(self, event):
        binds = {
            'Shift_L': self.not_send,
            'Return': self.add_message,
        }
        if event.keysym in binds.keys():
            binds[event.keysym]()

    def on_key_release(self, event):
        binds = {
            'Shift_L': self.may_send
        }
        if event.keysym in binds.keys():
            binds[event.keysym]()

    def not_send(self):
        self.send = False

    def may_send(self):
        self.send = True

    def print_messages(self):
        self.canvas.delete('all')
        for i, message in enumerate(self.messages):
            start = i * 50
            self.canvas.create_polygon(
                10, start + 50,
                20, start + 40,
                20, start + 10,
                len(message) * 8 + 40, start + 10,
                len(message) * 8 + 40, start + 50,
                fill='white'
            )
            self.canvas.create_text(30, start + 20, anchor='nw', text=message, font='Consolas 11')

    def get_message(self):
        message = self.entry.get(0.0, 'end')[:-2]
        self.entry.delete(0.0, 'end')
        return message

    def add_message(self):
        if not self.send:
            return
        message = self.get_message()
        message = re.sub('\s+', ' ', message)
        if message == '' or re.fullmatch('\s{2,}', message) is not None:
            return
        self.messages.append(message)
        self.print_messages()

    def entry_size_control(self, event=None):
        width = self.entry.winfo_width()
        line = width // 8
        text = self.entry.get(0.0, 'end')[:-1]
        if line != 0:
            count = (len(text) - 1) // line + len(text.split('\n')) - 1
            if count < 5:
                self.entry.config(height=count + 1)

    def run(self):
        self.tk.mainloop()


Interface(400, 500, 'Test').run()
