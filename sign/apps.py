from django.apps import AppConfig
from django.db.models.signals import post_save

class SignConfig(AppConfig):
    name = 'sign'
    verbose_name = 'sign'

    # def ready(self):
    #     from sign.util import process_message
    #     from util.mq import async_start_consume
    #     async_start_consume(process_message)