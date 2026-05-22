from django.contrib import admin
from .models import Mess

@admin.register(Mess)
class MessAdmin(admin.ModelAdmin):
    list_display = ('mess_name', 'owner_name', 'phone', 'food_per_day', 'subscription_rate', 'created_at')
    search_fields = ('mess_name', 'owner_name', 'phone', 'description')
    prepopulated_fields = {'slug': ('mess_name',)}
    list_filter = ('food_per_day', 'created_at')
