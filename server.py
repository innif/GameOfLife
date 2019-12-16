#! /usr/bin/python3

import json
import logging
import time
import threading

TURN = 0

class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.registered_player = 0
        self.player_a_handler = None
        self.player_b_handler = None


    def run(self):
        global TURN
        finished = False
        templates = []
        while not finished:
            self.player_a_handler.order_calc(templates)
            self.player_b_handler.order_calc(templates)
            while not (self.player_a_handler.calc_ack and self.player_b_handler.calc_ack):

                self.player_a_handler.handle_read()
                self.player_b_handler.handle_read()
                
                time.sleep(0.0001)
            
            
            self.player_a_handler.order_draw()
            self.player_b_handler.order_draw()

            templates = self.player_b_handler.template_request + self.player_a_handler.template_request
            TURN += 1
            

logging.basicConfig(filename='server.log', filemode='w', level=logging.INFO)
server = Server()


import asyncore

class GameHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, name):
        super().__init__(sock)
        self.calc_ack = False
        self.template_request = []
        self.name = name
        

    def handle_read(self):
        """
        handles calculate acknowledgements and template request messages.
        expects to be the messages a dictonary in json format.
        every message MUST have the type field set.
        template requests must also include a template requests field which conatains a list of points which shall be activated.
        """

        try:
            recv_data = self.recv(8192).decode()
        except BlockingIOError:
            return

        data = json.loads(recv_data)

        logging.info('Recieved data {} by \"{}\" in turn {}'.format(data, self.name, TURN))


        if type(data) != dict:
            logging.error('Wrong data format!')
            return
        
        if data['type'] == 'calculate ack':
            self.calc_ack = True
            logging.info('{} has finished xir\'s calculation in turn {}'.format(self.name, TURN))

        if data['type'] == 'template request:':
            logging.info('{} requests {}'.format(self.name, data[2:]))
            self.template_request += data['request']

    def order_calc(self, templates):

        logging.info('order {} to calculate {} the following templates were abstracted'.format(self.name, templates))

        message = {
            'type' : 'calculate order',
            'changes' : templates 
        }
        self.send(json.dumps(message).encode('ascii'))
    
    def order_draw(self):
        logging.info('order {} to draw'.format(self.name))

        message = {
            'type' : 'order draw'
        }
        self.send(json.dumps(message).encode('ascii'))
        
        self.calc_ack = False

class SocketServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):

        if server.registered_player == 1:
            server.player_b_handler = GameHandler(sock, 'PlayerB')
            print('accepted player b')
            server.registered_player +=1
            server.run()
            
        if server.registered_player == 0:
            server.player_a_handler = GameHandler(sock, 'PlayerB')
            print('accepted player a')
            server.registered_player +=1


socketserver = SocketServer('localhost', 1111)
asyncore.loop()


