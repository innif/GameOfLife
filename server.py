#! /usr/bin/python3

import json
import logging
import time
import threading
import asyncore

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
            

class GameHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, name):
        super().__init__(sock)
        self.calc_ack = False
        self.template_request = []
        self.name = name
        self.delimiter = '\n\n'
    

    def handle_read(self):
        """
        handles calculate acknowledgements and template request messages.
        expects to be the messages a dictonary in json format.
        every message MUST have the type field set.
        template requests must also include a template requests field which conatains a list of points which shall be activated.
        """

        try:
            recv_data = self.recv(4096).decode()
            
            if recv_data == '':
                return

            while recv_data[-2:] != self.delimiter:
                print(recv_data.split('\n'))
                recv_data += self.recv(4096).decode()
        except BlockingIOError:
            return

        # Make sure it end for an delimiter
        commands = recv_data.split(self.delimiter)

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

        for packet in queue:
            
            logging.info('Recieved data {} by \"{}\" in turn {}'.format(packet, self.name, TURN))

            if type(packet) != dict:
                logging.error('Wrong data format!')
                return
        
            if packet['type'] == 'calculate ack':
                self.calc_ack = True
                logging.info('{} has finished xir\'s calculation in turn {}'.format(self.name, TURN))

            if packet['type'] == 'template request':
                self.template_request += [packet['request']]
                logging.info('{} requests {}'.format(self.name, packet['request']))
        

    def send_message(self, message_type, **kwargs):
        kwargs['type'] = message_type
        message = json.dumps(kwargs).encode('ascii')
        self.send(message)
        self.send(self.delimiter.encode('ascii'))

    def order_calc(self, templates):
        logging.info('order {} to calculate {} the following templates were abstracted'.format(self.name, templates))
        self.send_message('calculate order', changes = templates)
        self.template_request = []
    
    def order_draw(self):
        logging.info('order {} to draw'.format(self.name))
        self.send_message('draw')
        self.calc_ack = False

    def send_delimiter(self):
        self.send(b'\n\n')

class SocketServer(asyncore.dispatcher):

    def __init__(self, host, port, gameserver):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.gameserver = gameserver

    def handle_accepted(self, sock, addr):

        if self.gameserver.registered_player == 1:
            self.gameserver.player_b_handler = GameHandler(sock, 'PlayerB')
            print('accepted player b')
            self.gameserver.registered_player +=1
            self.gameserver.run()
            
        if self.gameserver.registered_player == 0:
            self.gameserver.player_a_handler = GameHandler(sock, 'PlayerA')
            print('accepted player a')
            self.gameserver.registered_player +=1



if __name__ == '__main__':
    logging.basicConfig(filename='logging/server/server.log', filemode='a', level=logging.INFO)
    
    start_time = time.strftime('%d %b %Y %H:%M:%S', time.gmtime())
    logging.info('==='*30)
    logging.info('Started server at {}'.format(start_time))
    logging.info('==='*30)

    gameserver = Server()
    socketserver = SocketServer('localhost', 1111, gameserver)
    asyncore.loop()


