from django.db import models
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import Permission, User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Tag(models.Model):
   name = models.CharField(max_length=100, unique=True)
   def __str__(self):
       return self.name

class Game(models.Model):
    title = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[
        MinValueValidator(Decimal(0))
    ])
    logo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    url = models.URLField()
    tags = models.ManyToManyField(Tag)
    developer = models.ForeignKey(
        User,
        related_name='uploaded_games',
        on_delete=models.SET_NULL,
        null=True
    )
    players = models.ManyToManyField(User, through='GamePlayer', related_name='games')
    def sales_count(self):
        return self.players.count()
    def sales_sum(self):
        sales = self.transaction_set.filter(status=Transaction.COMPLETED)
        return sales.aggregate(models.Sum('amount'))['amount__sum'] or 0
    def __str__(self):
        return self.title

class GamePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    highscore = models.IntegerField(default=0)
    savedstate = models.TextField()
    class Meta:
        unique_together = ('game', 'user')
    def __str__(self):
        return self.game.title + ': ' + str(self.user)

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'tags', 'price', 'logo', 'url']
        widgets = {
            'description': Textarea(attrs={'rows': 10}),
        }

class Transaction(models.Model):
    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    startDate = models.DateTimeField(auto_now_add=True)
    completeDate = models.DateTimeField(null=True)
    payment_ref = models.IntegerField(null=True)
    PENDING = 0
    COMPLETED = 1
    CANCELLED = 2
    FAILED = 3
    PAYMENT_STATUS = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        (FAILED, 'Failed'),
    )
    status = models.IntegerField(choices=PAYMENT_STATUS, default=0)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    def __str__(self):
        game = str(self.game) if self.game else '<deleted game>'
        user = str(self.user) if self.user else '<deleted user>'
        return game + ': ' + user
