#! /usr/bin/python3

import json
import logging
import time
import threading
import asyncore


class Lobby(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.registered_player = 0
        self.player_a_handler = None
        self.player_b_handler = None
        self.is_full = False
        self.is_running = False
        self.turn = 0

    def add_player(self, player):
        if self.player_a_handler is None:
            self.player_a_handler = player
            return True
        
        if self.player_b_handler is None:
            self.player_b_handler = player
            self.is_full = True 
            return True

        return False

    def run(self):
        self.is_running = True
        finished = False
        templates = []
        while not finished:
            self.player_a_handler.order_calc(templates)
            self.player_b_handler.order_calc(templates)
            while not (self.player_a_handler.calc_ack and self.player_b_handler.calc_ack):

                if not self.player_a_handler.calc_ack:
                    self.player_a_handler.handle_read()

                if not self.player_b_handler.calc_ack:
                    self.player_b_handler.handle_read()            
            
            self.player_a_handler.calc_ack = False
            self.player_b_handler.calc_ack = False
            templates = self.player_b_handler.template_request + self.player_a_handler.template_request

            self.turn += 1
            

class PlayerHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, name, dispatcher):
        super().__init__(sock)
        self.intern_name = name
        self.username = None
        self.has_lobby = False
        self.is_in_game = False
        self.lobby = None

        self.dispatcher = dispatcher
        self.delimiter = '\n\n'

        self.calc_ack = False
        self.template_request = []

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

    def handle_read(self):
        """
        handles calculate acknowledgements and template request messages.
        expects to be the messages a dictonary in json format.
        every message MUST have the type field set.
        template requests must also include a template requests field which conatains a list of points which shall be activated.
        """

        #
        # recieve data until there is one packet finished
        # if there was no data recieved just skip so there are indexing errors
        #
        try:
            data = self.recv(4096).decode()
            
            if data == '':
                return

            while data[-2:] != self.delimiter:
                print(data.split('\n'))
                data += self.recv(4096).decode()
                
        except BlockingIOError:            
            return

        queue = self.split_packets(data)

        for packet in queue:
            self.handle_packet(packet)

    def handle_packet(self, packet):
        if self.is_in_game:
            logging.info('Recieved data {} by \"{}\" in turn {}'.format(packet, self.intern_name, self.lobby.turn))
        else:
            logging.info('Recieved data {} by \"{}\"'.format(packet, self.intern_name))


        # check if the json contains a dict
        if type(packet) != dict:
            logging.error('Wrong data format!')
            return
        
        #
        # handle the user registration
        # if username is set and the player has a lobby self.is_in_game will be set to true
        #
        if not self.is_in_game:

            #
            # Set username when username isn't already taken
            # when username is already taken inform the user about it
            #
            if packet.get('type', None) == 'set username':
                
                wanted_user_name = packet.get('username', None)
                if wanted_user_name == None:
                    logging.error('empty user name!')
                    return
                
                if self.dispatcher.request_user_name(wanted_user_name) == 'Accepted':
                    self.username = wanted_user_name
                    self.inform_username_accepted()
                else:
                    self.inform_username_already_taken()

            #
            # join a lobby by a lobby_name
            # if the lobby already exists and is not full yet then join it
            # if the lobby doesn't exist the dispatcher will create the lobby and make the player join
            # if the lobby exists but is already full the user will be informed
            #
            if packet.get('type', None) == 'join lobby':
               
                lobby_name =  packet.get('lobbyname', None)
                if lobby_name == None:
                    logging.error('empty lobby name!')
                    return
                
                lobby = self.dispatcher.join_lobby(lobby_name, self)

                if lobby is None:
                    self.inform_lobby_already_full()
                else:
                    self.inform_lobby_accepted()
                    self.lobby = lobby

            if packet.get('type', None) == 'list lobbys':

                lobbys = self.dispatcher.list_lobbys()
                self.inform_list_lobbys(lobbys)


            if self.lobby is not None:
                self.username = self.intern_name
            
            self.is_in_game = self.username is not None and self.lobby is not None

        #
        # handle the game interaction
        #
        else:

            #
            # player acknowledges a calculate process
            # set self.calc_ack to true
            # add the template request to the request list
            #
            if packet.get('type', None) == 'calculate ack':
                logging.info('{} has finished xir\'s calculation in turn {}'.format(self.intern_name, self.lobby.turn))
                self.calc_ack = True

                request = packet.get('request', None)

                if request == None:
                    logging.error('recieved empty template request by {} in turn {}'.format(self.intern_name, self.lobby.turn))
                    return

                self.template_request += request
                logging.info('{} requests {}'.format(self.intern_name, request))
  
    def order_calc(self, templates):
        logging.info('order {} to calculate {} the following templates were abstracted'.format(self.intern_name, templates))
        self.send_message('calculate order', changes = templates)
        self.template_request = []

    def inform_username_accepted(self):
        logging.info('username accepted {}'.format(self.intern_name))
        self.send_message('username', status = 'accepted')

    def inform_username_already_taken(self):
        logging.info('username already taken {}'.format(self.intern_name))
        self.send_message('username', status = 'already taken')

    def inform_lobby_accepted(self):
        logging.info('lobby accepted {}'.format(self.intern_name))
        self.send_message('lobby', status = 'accepted')

    def inform_lobby_already_full(self):
        logging.info('lobby already full {}'.format(self.intern_name))
        self.send_message('lobby', status = 'already full')

    def inform_list_lobbys(self, lobbylist):
        logging.info('list lobbys {}'.format(self.intern_name))
        self.send_message('lobbylist', lobbylist = lobbylist)

    def send_message(self, message_type, **kwargs):
            kwargs['type'] = message_type
            message = json.dumps(kwargs)
            message += self.delimiter
            self.send(message.encode('ascii'))

    def send_delimiter(self):
        self.send(b'\n\n')

class SocketDispatcher(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

        self.lobbys = {}
        self.players = []
        self.usernames = []

    def handle_accepted(self, sock, addr):
        player = PlayerHandler(sock, 'Player{}'.format(len(self.players)), self)
        self.players.append(player)

    def request_user_name(self, username):
        if username in self.usernames:
            return 'Denied'
        else:
            self.usernames.append(username)
            return 'Accepted'

    def join_lobby(self, lobby_name, player):
        lobby = self.lobbys.get(lobby_name, None)

        if lobby == None:
            self.lobbys[lobby_name] = Lobby()
            self.lobbys[lobby_name].add_player(player)
            return self.lobbys[lobby_name]
        
        if lobby.add_player(player):
            if lobby.is_full:
                lobby.start()
            return lobby
        
        return None

    def list_lobbys(self):
        result = []
        for key in self.lobbys.keys():
            result += [{
                'lobbyname': key,
                'joinable': not self.lobbys[key].is_full,
                'running': self.lobbys[key].is_running
                }]
        return result


if __name__ == '__main__':
    logging.basicConfig(filename='logging/server/server.log', filemode='a', level=logging.INFO)
    
    start_time = time.strftime('%d %b %Y %H:%M:%S', time.gmtime())
    logging.info('==='*30)
    logging.info('Started server at {}'.format(start_time))
    logging.info('==='*30)

    socketserver = SocketDispatcher('0.0.0.0', 1111)
    asyncore.loop()