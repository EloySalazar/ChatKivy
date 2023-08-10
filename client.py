import socket
import threading

import kivymd
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.textfield import MDTextField

from kivy.app import App
from kivy.base import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user = ""
n = 0

class Input_Text(TextInput):
    pass

class Sock(Screen):

    ip_w = ObjectProperty
    port_w = ObjectProperty
    user_w = ObjectProperty

    def send(text):
        print(text)
        


    def receive_messages(self):
        
        try:
            message = my_socket.recv(1024).decode('utf-8')

            if message == "@username":
                global user
                user = self.user_w.text
                my_socket.send(self.user_w.text.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error Ocurred")
            my_socket.close()
                

    def write_messages(self):
        while True:
            message = f"{self.user_w.text}: {input('')}"
            my_socket.send(message.encode('utf-8'))

    def verify(self):
        print(self.ip_w.text,int(self.port_w.text))
        try:
           
            my_socket.connect((self.ip_w.text,int(self.port_w.text)))

            self.receive_messages()

            self.manager.current ='2'
            self.manager.transition.direction = 'left'
            
        except :

            toast("Revise el Puerto y la IP")  
            return 1  


class Chat(Screen):
    message_w = ObjectProperty()
    chat_w = ObjectProperty()

    def start(self):
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def receive_messages(self):

        while True:

            global my_socket
            message = my_socket.recv(1024).decode('utf-8')
            try:
                if message == "@username":
                    global user
                    print(user)
                    my_socket.send(user.encode("utf-8"))
                else:
                    print(message)
                    self.chat_w.insert_text("\n"+message)
        
            except:
                print("An error Ocurred")
                my_socket.close()
                 
            

    

    def send(self):
        Sock.send(self.message_w.text)
        self.chat_w.insert_text("\n"+self.message_w.text)

        global my_socket
        message = f"{user}: {self.message_w.text}"
        my_socket.send(message.encode('utf-8'))
        self.message_w.text = ""
       




sm = ScreenManager()
chat = Chat(name='2')
sm.add_widget(Sock(name='1'))
sm.add_widget(chat)


        
class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        kv = Builder.load_file("manager.kv")
        return kv



main = App()
main.run()