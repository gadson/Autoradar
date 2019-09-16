from django.contrib import admin
from .models import Geo, movement, events, Profile, Push_ID


@admin.register(Geo)
class GeoAdmin(admin.ModelAdmin):
   list_display = ['ID_obj', 'name', 'dop','telephone','email' ]

# Register your models here.
@admin.register(movement)
class movementAdmin(admin.ModelAdmin):
   list_display = ['ID_obj', 'datetime', 'Latitude', 'Longitude']

@admin.register(events)
class eventsAdmin(admin.ModelAdmin):
   list_display = ['ID_obj', 'datetime', 'event', 'dop', 'logic']

@admin.register(Profile)
class GeoAdmin2(admin.ModelAdmin):
   list_display = [ 'user', 'phone','zoom','select' ]

@admin.register(Push_ID)
class PUSH(admin.ModelAdmin):
   list_display = [ 'User', 'ID_Push' ]

# Register your models here.
