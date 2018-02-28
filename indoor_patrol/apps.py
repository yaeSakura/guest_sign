from django.apps import AppConfig


class IndoorPatrolConfig(AppConfig):
    name = 'indoor_patrol'

    # def ready(self):
    #     # from indoor_patrol.consumer import consumer
    #     from indoor_patrol.consumer_copy import async_start_consume
    #     from indoor_patrol.util import save_spot_msg
    #     async_start_consume(save_spot_msg)
    #     print('Indoor_patrol is ready over')