#! /usr/bin/env python 
# -*- coding:utf-8 -*-
import pika
import logging
import threading

logger = logging.getLogger(__name__)

class Consumer():
    EXCHANGE = 'location'
    EXCHANGE_TYPE = 'direct'
    # PUBLISH_INTERVAL = 1
    QUEUE = 'text'
    ROUTING_KEY = 'hola'

    def __init__(self, event=None, process_func=None):
        credentials = pika.PlainCredentials("heziqi", "heziqi")
        conn_params = pika.ConnectionParameters("47.95.208.252",
                                                virtual_host="test",
                                                credentials=credentials,
                                                connection_attempts=3,
                                                heartbeat=3600)

        self._process_func = process_func
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._conn_params = conn_params

    def connect(self):
        print('Connecting to ', self._conn_params.host)
        if self._connection:
            self._connection.connect()
        else:
            self._connection = pika.SelectConnection(parameters=self._conn_params,
                                                     on_open_callback=self.on_connection_open,
                                                     on_close_callback=self.on_connection_closed,
                                                     stop_ioloop_on_close=False)
        return self._connection

    def on_connection_open(self, unused_connection):
        print('Connection opend')
        self.open_channel()

    def on_connection_closed(self,connection, reply_code, reply_text):
        print('Connection closed, reopening in 1 seconds: (%s) %s' % (reply_code, reply_text))
        self._connection.add_timeout(1, self.reconnect)

    def open_channel(self):
        print('Create a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        print('Channel opened')
        self._channel = channel
        self.setup_exchange(self.EXCHANGE)

    def setup_exchange(self, exchange_name):
        print('Declaring exchange ', exchange_name)
        self._channel.exchange_declare(callback=self.on_exchange_declareok,
                                       exchange=exchange_name,
                                       exchange_type=self.EXCHANGE_TYPE,
                                       passive=False,
                                       durable=True,
                                       auto_delete=False)

    def on_exchange_declareok(self, unused_frame):
        print('Exchange declared')
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        print('Declarig queue ', queue_name)
        self._channel.queue_declare(callback=self.on_queue_declareok,
                                    queue=queue_name)

    def on_queue_declareok(self, method_frame):
        print('Binding {} to {} with {}'.format(self.EXCHANGE,
                                                      self.QUEUE,
                                                      self.ROUTING_KEY))
        self._channel.queue_bind(callback=self.on_bindok,
                                 queue=self.QUEUE,
                                 exchange=self.EXCHANGE,
                                 routing_key=self.ROUTING_KEY)

    def on_bindok(self, unused_frame):
        print('Queue bound')
        self.start_consuming()

    def start_consuming(self):
        print('Issuing consumer related RPC commands')
        self._consumer_tag = self._channel.basic_consume(consumer_callback=self.on_message,
                                                         queue=self.QUEUE)

    def on_message(self, unused_channel, basic_deliver, properties, body):
        print('Recevied message # {} from {}：{}'.format(
            basic_deliver.delivery_tag, properties.app_id, body
        ))
        if self._process_func:
            self._process_func(body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        print('Acknowlegding message {}'.format(delivery_tag))
        self._channel.basic_ack(delivery_tag)

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

def async_start_consume(f=None):
    t = threading.Thread(target=start_consume, args=(f,))
    t.daemon = True
    t.start()

def start_consume(f=None):
    consumer = Consumer(process_func=f)
    consumer.run()

def main():
    async_start_consume()

if __name__ == "__main__":
    LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                                '-35s %(lineno) -5d: %(message)s')
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    main()