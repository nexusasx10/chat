from client import Client
from tkinter import Tk, Entry, Label, Button, Text
from sys import argv


class ClientGUI:

    def __init__(self):
        self.client = Client(argv[1] if len(argv) == 2 else 'localhost')
        self.window = Tk()
        self.buffer_size = 5
        self.window.geometry('400x200')
        self.window.title('Chatters')
        self.ip_ent = Entry(master=self.window)
        self.name_ent = Entry(master=self.window)
        self.input_ent = Entry(master=self.window)
        self.output_ent = Text(master=self.window, width=45, height=5)
        self.buffer = list()
        self.log = None
        self.get_start_window()
        self.window.mainloop()

    def connect(self):
        self.client.server_ip = self.ip_ent.get()
        self.client.name = self.name_ent.get()
        self.client.connect()
        self.log = open('{}.txt'.format(self.client.server_ip), 'a')
        self.clear_window()
        self.get_chat_window()
        self.window.bind('<Return>', self.send)
        self.window.protocol('WM_DELETE_WINDOW', self.close)
        self.client.update_thread.start()
        self.update()

    def update(self):
        msgs_len = len(self.client.new_messages)
        if msgs_len != 0:
            with self.client.lock:
                for i in range(msgs_len):
                    self.buffer.append(self.client.new_messages.pop(0))
            while len(self.buffer) > self.buffer_size:
                self.log.write('{}\n'.format(self.buffer.pop(0)))
            self.output_ent.delete(1.0, 'end')
            buf_len = len(self.buffer)
            if buf_len != 0:
                to_show = ''
                for i in range(buf_len):
                    to_show += self.buffer[i] + '\n'
                self.output_ent.insert(1.0, to_show)
        self.window.after(100, self.update)

    def send(self, e=None):
        msg = self.input_ent.get().strip()
        if len(msg) > 0:
            self.client.send_message(self.input_ent.get())
        self.input_ent.delete(0, 'end')

    def disconnect(self):
        self.window.after_cancel(self.update)
        self.client.disconnect()
        while len(self.buffer) > 0:
            self.log.write(self.buffer.pop(0) + '\n')
        self.log.close()

    def connect_local(self):
        self.client.server_ip = 'localhost'
        self.client.name = 'Vadim'
        self.client.connect()
        self.log = open('{}.txt'.format(self.client.server_ip), 'a')
        self.clear_window()
        self.get_chat_window()
        self.window.bind('<Return>', self.send)
        self.window.protocol('WM_DELETE_WINDOW', self.close)
        self.client.update_thread.start()
        self.update()

    def clear_window(self):
        for wid in self.window.winfo_children():
            wid.place_forget()

    def get_start_window(self):
        Label(master=self.window, text='IP:').place(x=10, y=10)
        self.ip_ent.place(x=100, y=10)
        Label(master=self.window, text='Name:').place(x=10, y=50)
        self.name_ent.place(x=100, y=50)
        Button(master=self.window, text='Connect',
               command=self.connect).place(x=10, y=100)
        Button(master=self.window, text='Local',
               command=self.connect_local).place(x=100, y=100)

    def get_chat_window(self):
        self.input_ent.place(x=10, y=100)
        self.output_ent.place(x=10, y=10)
        Button(master=self.window, text='Send', command=self.send).place(
            x=10, y=150)
        Button(master=self.window, text='Leave',
               command=self.leave).place(x=50, y=150)

    def leave(self):
        self.disconnect()
        self.clear_window()
        self.get_start_window()

    def close(self):
        if self.client.connected:
            self.disconnect()
        self.window.destroy()


if __name__ == '__main__':
    CLIENT_GUI = ClientGUI()
