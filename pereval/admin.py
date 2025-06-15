from django.contrib import admin
from .models import Pereval, User, Coords, Level, Image

@admin.register(Pereval)
class PerevalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'add_time')
    search_fields = ('title', 'user__email')

admin.site.register(User)
admin.site.register(Coords)
admin.site.register(Level)
admin.site.register(Image)