from django.contrib import admin

from .models import Game, GamePlayer, Transaction, Tag

admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(Transaction)
admin.site.register(Tag)
