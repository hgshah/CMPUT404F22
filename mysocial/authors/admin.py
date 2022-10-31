from django.contrib import admin

from .models import Author


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('official_id',)


admin.site.register(Author, AuthorAdmin)
