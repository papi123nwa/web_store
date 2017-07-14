from django.shortcuts import render, get_object_or_404
from gamestore.models import Game
from django.http import HttpResponse
import json

def get_games(request):
    games = Game.objects.order_by('id').values('id','title')
    dict = {}
    for game in games:
        dict[game['id']] = game['title']
    json_content = json.dumps(dict, indent=2)
    return HttpResponse(json_content, content_type='application/json')

def get_game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    dict = {
            "title": game.title,
            "price": str(game.price),
            "tags": list(game.tags.values_list('name',flat=True)),
            "developer": game.developer.username,
            "description": game.description
        }
    json_content = json.dumps(dict, indent=2)
    return HttpResponse(json_content, content_type='application/json')