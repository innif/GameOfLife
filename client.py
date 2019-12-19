#! usr/bin/python3

import socket
import json
import logging
import argparse

from field import Field
from display import Display
from template import Template
from cache import Cache

import figures
import pygame
import colorsets


class NetworkClient:
    def __init__(self, cache, server_ip = 'localhost', port = 1111):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, port))
        # delimiter
        self.delimiter = '\n\n'
        # the tcp socker to the server
        self.sock = sock
        # a queue that contains the json objs which where sent by the game server
        self.queue = []
        self.cache = cache

    def send_message(self, message_type, **kwargs):
        kwargs['type'] = message_type
        message = json.dumps(kwargs)
        message += self.delimiter
        self.sock.send(message.encode('ascii'))

    def send_template_request(self, templ, position):
        self.send_message('template request', request = (templ._pointlist, position))

    def send_calc_ack(self, requests):
        self.send_message('calculate ack', request=requests)

    def request_username(self, username):
        self.send_message('set username', username = username)

    def request_lobbylist(self):
        self.send_message('list lobbys')

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
                self.cache.calculate_one_tick()

        return changes    

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

    def wait_list_lobbys(self):
        while True:
            if self.queue != []:
                lobby_answer = self.queue.pop(0)
                if lobby_answer.get('type', None) == 'lobbylist':
                    return lobby_answer.get('lobbylist', None)
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
                print('JSON decoder error:')
                print(command)
                print(er)

        return queue

def start():

    parser = argparse.ArgumentParser(description='Start the game of life with a given server and a given port')
    parser.add_argument('domain', metavar='d', type = str,  help='the domain of the server')
    parser.add_argument('port', metavar='p', type = int,  help='the port where the server hosts the socket')
    args = parser.parse_args()

    size = 100, 100

    f = Field(size=size, initValue=0)

    t = Template('GLIDER', figures.glider_diagonal_ne)
    #f.place_template(t, (5, 5))
    #fill_random(f, seed=0)

    d = Display(f.size, (1200,900), 800)
    d.set_field(f)
    d.set_colors(colorsets.light_gray)
    #f.load_from_file('field.f')
    d.load_template(t)

    cache = Cache(f)

    c = NetworkClient(cache, args.domain, args.port)

    username_set = False
    while not username_set:
        username = input('Set username: ')
        c.request_username(username)
        username_set = c.wait_username_accept()
        if not username_set:
            print('Username already taken!')

    c.request_lobbylist()
    lobbys = c.wait_list_lobbys()

    print('Lobbys:')
    print(lobbys)
    if not lobbys:
        print('== No lobbys exist yet ==') 
    print('*'*30)
    for lobby in lobbys:
        print('name:     {}'.format(lobby.get('lobbyname', None)))
        print('joinable: {}'.format(lobby.get('joinable', None)))
        print('running:  {}'.format(lobby.get('running', None)))
        print('*'*30)
    
    lobby_joined = False
    while not lobby_joined:
        lobby = input('Set lobby: ')
        c.join_lobby(lobby)
        lobby_joined = c.wait_join_lobby_accept()
        if not lobby_joined:
            print('lobby already full!')


    while(True):
        d.draw_field(f)
        changes = c.wait_calc_order()

        for change in changes:
            f.place_pointlist(change[0], change[1])

        requested_changes = [[templ._pointlist, pos] for templ, pos in d.handle_user_events() if pos is not None]

        c.send_calc_ack(requested_changes)

        cache_is_dirty = changes != []
        f = cache.get_next(dirty = cache_is_dirty)


if __name__ == "__main__":
    import cProfile
    cProfile.run('start()')
    #start()