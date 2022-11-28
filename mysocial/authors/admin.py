from django.contrib import admin

from authors.models.author import Author
from authors.models.remote_node import RemoteNode


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('official_id',)
    list_display = ('__str__', 'official_id')


admin.site.register(Author, AuthorAdmin)

# let's register author in RemoteNode here to prevent circular dependency
RemoteNode.author_class = Author


class RemoteNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'author_id', 'remote_username', 'status')


admin.site.register(RemoteNode, RemoteNodeAdmin)
