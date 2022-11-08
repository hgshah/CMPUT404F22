from django.contrib import admin

from authors.models.author import Author


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('official_id',)
    list_display = ('__str__', 'official_id')


admin.site.register(Author, AuthorAdmin)
