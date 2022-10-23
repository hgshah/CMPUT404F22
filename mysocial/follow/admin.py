from django.contrib import admin

from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Follow, FollowAdmin)
