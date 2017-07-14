from hashlib import md5
from hmac import compare_digest
from os import environ
import json

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest, # 400
    HttpResponseForbidden,  # 403
    HttpResponseNotFound,   # 404
    HttpResponseServerError,# 500
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from gamestore.models import Game, GameForm, GamePlayer, Transaction, Tag

def index(_unused):
    return redirect('browse_games')

def browse_games(request, owned_only):
    tags = request.GET.get('tags')
    user = request.user

    if(owned_only):
        games = user.games.all()
    else:
        games = Game.objects.all()

    if(tags != None):
        tags = tags.split(' ')
        for tag in tags:
            tagObject = Tag.objects.get(name=tag)
            games = games.filter(tags=tagObject)

    all_tags = Tag.objects.values_list('name', flat=True)
    return render(request, 'browse_games.html', {'games': games, 'tags': all_tags, 'selected_tags': tags})

def detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    owned = user.games.filter(id=game_id).exists() if user.is_authenticated else False
    scores = GamePlayer.objects.filter(game=game).values_list('user__username','highscore').order_by('-highscore')
    return render(request, 'game_details.html', {'game': game, 'owned': owned, 'scores': scores})

@login_required
def buy_game(request, game_id):
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    owned = request.user.games.filter(id=game_id).exists() if user.is_authenticated else False
    if owned:
        return redirect('detail', game_id=game_id)
    transaction = Transaction(user=user, game=game)
    transaction.amount = game.price
    transaction.save()
    pid = transaction.id
    sid = environ['PAYMENT_SELLER_ID']
    amount = game.price
    payment_secret_key = environ['PAYMENT_SECRET_KEY']
    checked_msg = 'pid={}&sid={}&amount={}&token={}'.format(pid, sid, amount, payment_secret_key)
    m = md5()
    m.update(checked_msg.encode('utf-8'))
    checksum = m.hexdigest()
    url = request.build_absolute_uri(reverse('payment', kwargs={'game_id': game_id}))
    payment_info = {'pid': pid, 'sid': sid, 'amount': amount, 'checksum': checksum, 'url': url}
    return render(request, 'buy_game.html', {'payment_info': payment_info, 'game': game})

@login_required
def edit_game(request, game_id):
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    if game.developer != user:
        return HttpResponseForbidden('User is not developer of this game')
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('developer_profile')
    else:
        form = GameForm(instance=game)
    context = {'user': user, 'form': form}
    return render(request,'edit_game.html',context)

@login_required
def payment(request, game_id):
    # Get parameters
    try:
        pid = int(request.GET['pid'])
        ref = int(request.GET['ref'])
        result = request.GET['result']
        checksum = request.GET['checksum']
    except:
        return HttpResponseBadRequest('Missing or invalid parameters')

    # Verify validity
    payment_secret_key = environ['PAYMENT_SECRET_KEY']
    checked_msg = 'pid={}&ref={}&result={}&token={}'.format(pid, ref, result, payment_secret_key)
    m = md5()
    m.update(checked_msg.encode('utf-8'))
    calculated_checksum = m.hexdigest()
    if not compare_digest(checksum, calculated_checksum):
        return HttpResponseBadRequest('Invalid checksum')

    # Check transaction
    try:
        transaction = Transaction.objects.get(id=pid)
    except:
        return HttpResponseServerError('Transaction not found')
    if transaction.status != transaction.PENDING:
        return HttpResponseBadRequest('Transaction already finished')
    user = transaction.user
    game = transaction.game
    if user != request.user:
        return HttpResponseBadRequest('User does not match')
    if game.id != int(game_id):
        return HttpResponseBadRequest('Game does not match')
    transaction.payment_ref = ref
    transaction.completeDate = timezone.now()

    # Update status
    if result == 'error':
        transaction.status = transaction.FAILED
        transaction.save()
        return HttpResponse('Payment service error')
    if result == 'cancel':
        transaction.status = transaction.CANCELLED
        transaction.save()
        return HttpResponse('You cancelled the payment')
    if result == 'success':
        transaction.status = transaction.COMPLETED
        transaction.save()
        gameplayer = GamePlayer(game=game, user=user)
        gameplayer.save()
        return redirect('detail', game_id=game_id)
    return HttpResponseBadRequest('Unrecognized result')

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required
def developer_profile(request):
    user = request.user
    if not user.uploaded_games.exists():
        return HttpResponseForbidden('User is not a developer')
    games = user.uploaded_games.all()
    total_sales = sum(map(lambda game: game.sales_sum(), games))
    return render(request, 'developer_profile.html', {'games': games, 'total_sales': total_sales})

@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            addedGame = form.save(commit=False)
            addedGame.developer = request.user
            addedGame.save()
            form.save_m2m()
            return redirect('browse_games')
    else:
        form = GameForm()
    return render(request, 'add_game.html', {'form': form})

@login_required
def message(request, game_id):
    print(request.body, flush=True)
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    try:
        gameplayer = GamePlayer.objects.get(game=game, user=user)
    except GamePlayer.DoesNotExist:
        return HttpResponseForbidden('User has not bought the game')
    try:
        message = json.loads(request.body.decode('utf-8'))
    except UnicodeError:
        return HttpResponseBadRequest('Invalid UTF-8')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    if message['messageType'] == 'SCORE':
        new_score = message['score']
        if new_score > gameplayer.highscore:
            gameplayer.highscore = new_score
            gameplayer.save()
        return HttpResponse(status=204)
    elif message['messageType'] == 'SAVE':
        gameplayer.savedstate = json.dumps(message['gameState'])
        gameplayer.save()
        return HttpResponse(status=204)
    elif message['messageType'] == 'LOAD_REQUEST':
        state = gameplayer.savedstate
        response = {}
        if state != '':
            response['messageType'] = 'LOAD'
            response['gameState'] = json.loads(state)
        else:
            response['messageType'] = 'ERROR'
            response['info'] = 'No saved state available'
        return JsonResponse(response)
    else:
        return HttpResponseBadRequest('Unrecognized message type')

@login_required
def remove_game(request, game_id):
    request.user.uploaded_games.get(pk=game_id).delete()
    if request.user.uploaded_games.exists():
        return redirect('developer_profile')
    else:
        return redirect('browse_games')
