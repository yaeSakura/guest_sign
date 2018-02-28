from django.contrib import admin
from indoor_patrol.models import *

# Register your models here.

admin.site.register(Route)
admin.site.register(Plan)
admin.site.register(Guard)
admin.site.register(Terminal)