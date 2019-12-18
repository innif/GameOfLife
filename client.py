#! usr/bin/python3

import socket
import json
import logging
import argparse

from field import Field
from display import Display
from template import Template

import figures
import pygame
import colorsets


class NetworkClient:
    def __init__(self, server_ip = 'localhost', port = 1111):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, port))
        # delimiter
        self.delimiter = '\n\n'
        # the tcp socker to the server
        self.sock = sock
        # a queue that contains the json objs which where sent by the game server
        self.queue = []

    def send_message(self, message_type, **kwargs):
        kwargs['type'] = message_type
        message = json.dumps(kwargs)
        message += self.delimiter
        self.sock.send(message.encode('ascii'))

    def send_template_request(self, templ, position):
        self.send_message('template request', request = (templ._pointlist, position))

    def send_calc_ack(self):
        self.send_message('calculate ack')

    def request_username(self, username):
        self.send_message('set username', username = username)

    def join_lobby(self, lobbyname):
        self.send_message('join lobby', lobbyname = lobbyname)

    def wait_calc_order(self):
        changes = None
        while changes is None:
            if self.queue != []:
                order = self.queue.pop(0)
                if order['type'] == 'calculate order':
                    changes = order['changes']
            else:
                self.poll_server_packets()
            
        return changes    

    def wait_draw_order(self):
        draw_command_given = False
        while not draw_command_given:
            if self.queue != []:
                order = self.queue.pop(0)
                if order['type'] == 'draw':
                    draw_command_given = True
            else:
                self.poll_server_packets()

    def wait_username_accept(self):
        while True:
            if self.queue != []:
                username_answer = self.queue.pop(0)
                if username_answer.get('type', None) == 'username':
                    status = username_answer.get('status', None)
                    if status == 'accepted':
                        return True
                    elif status == 'already taken':
                        return False
            else:
                self.poll_server_packets()
    
    def wait_join_lobby_accept(self):
        while True:
            if self.queue != []:
                lobby_answer = self.queue.pop(0)
                if lobby_answer.get('type', None) == 'lobby':
                    status = lobby_answer.get('status', None)
                    if status == 'accepted':
                        return True
                    elif status == 'already full':
                        return False
            else:
                self.poll_server_packets()

    def poll_server_packets(self):
        '''
        polls server packets and adds them into the queue after they were converted from json objects
        '''
        # Make sure it end for an delimiter
        data = self.sock.recv(4096).decode()

        if data == '':
            return

        while data[-2:] != self.delimiter:
            data += self.sock.recv(4096).decode()

        new_commands = self.split_packets(data)
        self.queue += new_commands
 
    def split_packets(self, data):
        commands = data.split(self.delimiter)

        queue = []
        for command in commands:
            if command == '':
                continue

            try:
                obj = json.loads(command)
                queue.append(obj)
            except json.decoder.JSONDecodeError as er:
                print(command)
                print(er)

        return queue

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Start the game of life with a given server and a given port')
    parser.add_argument('domain', metavar='d', type = str,  help='the domain of the server')
    parser.add_argument('port', metavar='p', type = int,  help='the port where the server hosts the socket')
    args = parser.parse_args()

    c = NetworkClient(args.domain, args.port)

    username_set = False
    while not username_set:
        username = input('Set username: ')
        c.request_username(username)
        username_set = c.wait_username_accept()
        if not username_set:
            print('Username already taken!')

    lobby_joined = False
    while not lobby_joined:
        lobby = input('Set lobby: ')
        c.join_lobby(lobby)
        lobby_joined = c.wait_join_lobby_accept()
        if not lobby_joined:
            print('lobby already full!')

    size = 100, 100

    f = Field(size=size, initValue=0)

    t = Template('GLIDER', figures.gliderDiagonalNE)
    f.placeTemplate(t, (5, 5))
    # f.fillRandom(seed=0)

    d = Display(f.getSize(), 1000)
    d.setField(f)
    d.setColors(colorsets.lightGray)
    #f.loadFromFile('field.f')
    d.loadTemplate(t)


    while(True):
        d.drawField(f)
        for templ, position in d.mainloop():
            c.send_template_request(templ, position)
        changes = c.wait_calc_order()
        for change in changes:
            f.placePointlist(change[0], change[1])
        c.send_calc_ack()
        c.wait_draw_order()
        f.update()