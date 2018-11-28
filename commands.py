import tkinter as tk
import configparser
import hasher
import os

command_list = []

class Command:          #Command inis for custom success/failure messages?

    success_message = ' successfully'
    failure_message = ', but it failed'

    def __init__(self, prefix='/', name='', function=None, syntax=None):
        self.prefix = prefix
        self.name = name
        self.fname = prefix+name
        self.function = function
        self.syntax = syntax

    def execute(self, *args):
        if self.function(*args) == 0:
            return self.success_message
        else:
            return self.failure_message


def load_commands():
    command_file = open('commands.txt', 'r')
    for command in command_file:
        command = command.replace('\n', '')         #same thing, check how to do better
        if ' ' in command:
            prefix, name = command.split(' ')
        else:
            prefix = command[0]
            name = command[1:]
        c = Command(prefix, name)
        command_list.append(c)
        setattr(c, 'function', eval(c.name+'_function'))


def nick_function(client, nick, server):
    if client.name == ' ':      #New client, check for people choosing space as nickname
        client.name = nick
        print(server.new_client_message.replace('[CLIENTNAME]', client.name))
        server.send_to_all(server.new_client_message.replace('[CLIENTNAME]', client.name))
    elif True:#valid_nick(nick):
        print(server.client_changed_nick_message.replace('[NEWCLIENTNAME]', nick).replace('[CLIENTNAME]', client.name))
        server.send_to_all(server.client_changed_nick_message.replace('[NEWCLIENTNAME]', nick).replace('[CLIENTNAME]', client.name))
        client.name = nick
        return 0
    else: 
        return 1

def register_function(client, password, server):
    try:
        user_folder = _create_user_folder(client.name)
        hashed_password, salt = _hash_password(password)
        _create_login_ini(hashed_password, salt, user_folder)
    except FileExistsError:
        return 1
    return 0

def _hash_password(password):
    salt = hasher.create_salt()
    hashed_password = hasher.hash(password, salt)
    return hashed_password, salt

def _create_login_ini(hashed_password, salt, user_folder):
    config = configparser.ConfigParser()
    config['LOGIN_INFO'] = {}
    config['LOGIN_INFO']['pass_hash'] = hashed_password
    config['LOGIN_INFO']['salt'] = salt
    login_file = open(user_folder+'\\login.ini', 'w')       #Look up on closing file necessity (with?)
    config.write(login_file)
    return config

def _create_user_folder(client_name):
    user_folder = "users\\"+client_name     #Protect against invalid windows folder names
    os.makedirs(user_folder)
    return user_folder

def login_function(client, password, server):
    user_folder = "users\\"+client.name
    if not _is_registered(user_folder):
        client.send('--Nickname not registered. Use "/register [password]" to register this nickname--')
        return 1
    hashed_password, salt = _get_login_info(user_folder)
    input_pass = hasher.hash(password, salt)
    if input_pass == hashed_password:
        client.send('--Login successful--')
        return 0
    else:
        client.send('--Wrong password--')
        return 1

def _is_registered(folder):
    if os.path.isdir(folder):
        return True
    else:
        return False

def _get_login_info(folder):
    config = configparser.ConfigParser()
    config.read(folder+'\\login.ini')
    salt = config['LOGIN_INFO']['salt']
    hashed_password = config['LOGIN_INFO']['pass_hash']
    return hashed_password, salt


load_commands()
            

