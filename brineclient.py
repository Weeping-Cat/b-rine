import os
import socket
import tkinter as tk
from threading import Thread

class Launcher():

    host_ip = '85.245.77.162'
    host_port = 7700

    def __init__(self):
        self.connect()
        self.username = 'dev' ##################
        self.set_username(self.username)
        self.launch_BRINE()

    def connect(self):
        s = socket.socket()
        try:
            s.connect((self.host_ip, self.host_port))
        except ConnectionRefusedError:                                  #Build offline mode?
            s.connect((socket.gethostbyname(socket.gethostname()), self.host_port))
        self.socket = s

    def set_username(self, username=None):
        if username is None:
            username = input()
        self.username = username

    def launch_BRINE(self):
        app = BRINEClient(self.socket, self.username)
        app.root.title('B-RINE')
        app.root.mainloop()
        self.app = app

S = 10 #CHANGE THIS ASAP
class BRINEClient():

    def __init__(self, s, username):
        self.scrollbar_locked = False
        self.nightmode = False
        self.s = s
        self._create_window()
        self._create_frame()
        self._create_widgets()
        self._bind_keyboard_events()
        self.start_listen_thread()
        self.s.send(('/nick '+ username).encode())

    def _create_window(self):
        self.root = tk.Tk()
        self.root.config(bg="#000000")
        self.root.iconbitmap('data\\icon.ico')
        self.root.resizable(False, False)

    def _create_frame(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0)

    def _create_widgets(self):
        self._create_send_button()
        self._create_side_buttons()
        self._create_text_entry()
        self._create_text_display()

    def _create_send_button(self):
        self.send_button = tk.Button(self.frame, text='Send', command=self.send_message)
        self.send_button.grid(row=S, column=1)

    def _create_text_entry(self):
        e = tk.Entry(self.frame)
        e.grid(row=S, column=0, sticky='nsew')
        self.e = e

    def _create_text_display(self):
        display = tk.Text(self.frame)
        display.grid(row=0, column=0, rowspan=S, sticky='nsew')
        self._create_scrollbar(display)
        self.display = display

    def _create_scrollbar(self, text_display):      #Look at rightclick again, consider brine classes for widgets
        scroll = tk.Scrollbar(self.frame, orient="vertical", command=text_display.yview)
        text_display.configure(yscrollcommand=scroll.set)
        scroll.config(command=text_display.yview)
        scroll.grid(row=0, column=1, rowspan=S, sticky='nsew')
        scroll.popup_menu = tk.Menu(scroll, tearoff=0)
        scroll.popup_menu.add_command(label="Lock",
                                    command=self.set_scrollbar_locked)
        scroll.bind("<Button-3>", self._scrollbar_rightclick_menu)
        self.scrollbar = scroll

    def _scrollbar_rightclick_menu(self, event):
        self.scrollbar.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def set_scrollbar_locked(self):
        self.scrollbar_locked = not self.scrollbar_locked

    def _create_side_buttons(self):         #Look into changing from gif to other
        btn_dir = 'data\\buttons\\'
        row = 0
        column = 2
        for gif in os.listdir(btn_dir):
            if '.gif' not in gif:
                continue
            btn_img = tk.PhotoImage(file=btn_dir+gif)
            gif_name = gif.replace('.gif', '')
            setattr(self, gif_name+'_button', tk.Button(self.frame, image=btn_img))
            btn = getattr(self, gif_name+'_button')
            btn.image = btn_img
            try:
                btn.config(command=getattr(self, gif_name+'_button_command'))
            except AttributeError:
                print('No command found for '+gif_name+' button!')
            btn.grid(row=row, column=column)
            row += 1
            if row > 11:
                print('Too many buttons! x'+str(row-11))

    def moon_button_command(self):
        self.set_nightmode()

    def pet_button_command(self):
        print('PET!')

    def _bind_keyboard_events(self):
        self.e.bind("<Return>", self.send_message)
  
    def send_message(self, source='btn'):
        self.s.send(self.e.get().encode())
        self.e.delete(0, tk.END)

    def set_nightmode(self):                                    ##Change and complete, the exceptions are just because lazy iterating through all widgets in the frame
        self.nightmode = not(self.nightmode)
        for widget in self.frame.grid_slaves():
            try:
                widget.config(bg='#000000', fg='#ffffff') if self.nightmode else widget.config(bg='#ffffff', fg='#000000')
            except tk.TclError:
                pass
            except AttributeError:
                pass

    def start_listen_thread(self):
        listen_thread = Thread(target = self.listen_for_messages)
        listen_thread.start() 

    def listen_for_messages(self):
        while True:
            message = self.s.recv(1024).decode()
            self.on_message_received(message)

    def on_message_received(self, message):
        self.display_message(message)

    def display_message(self, message):
        self.display.insert(tk.END, message+'\n')
        if not self.scrollbar_locked:
            self.display.see("end")

l = Launcher()

