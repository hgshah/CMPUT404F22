from django.contrib import admin
from .models import Like, Inbox
# Register your models here.

#admin.site.Register(Liked)
admin.site.register(Like)
admin.site.register(Inbox)
