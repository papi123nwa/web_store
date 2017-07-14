

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from gamestore.models import Game, GameForm, GamePlayer, Transaction
from . import views


class ModelsTest(TestCase):


    def testProfile(self):
        self.us1 = User.objects.create(username="user1", password="12345678", email="xx@gmail.com")

        self.us2 = User.objects.create(username="user2")


        # Test creation
        self.assertEqual(self.us1.__str__(), 'user1')
        self.assertEqual(self.us1.password, '12345678')
        self.assertEqual(self.us1.email, 'xx@gmail.com')
        #
        # # Test update
        self.us1.username = "user7"
        self.assertEqual(self.us1.__str__(), "user7")
        self.us1.password = "00000000"
        self.assertEqual(self.us1.password, "00000000")

        self.us1.email = "email@gmail.com"
        self.assertEqual(self.us1.email, "email@gmail.com")




    def testPlayedMatch(self):
        self.us1 = User.objects.create(username="profile1", password="12345678", email="xx@gmail.com")


        game1 = Game.objects.create(title="Clash of Clans", description="No descr", url="http://www.google.com", price=
                                     3, logo="http://www.image.com",
                                    developer=self.us1)
        self.us2 = User.objects.create(username="profile2", password="12345678", email="xxxx@gmail.com")

        game2 = Game.objects.create(title="Fifa 16", description="No descr", url="http://www.yahoo.com", price=
                                    3, logo="http://www.image.com",
                                    developer=self.us2)

        playedmatch1 = GamePlayer.objects.create(highscore=500, user=self.us1, game=game1)

    #     # Test creation
        self.assertEqual(playedmatch1.highscore, 500)
        self.assertEqual(playedmatch1.game, game1)
        self.assertEqual(playedmatch1.user, self.us1)
    #
    #     # Test update
        playedmatch1.score = 5000
        self.assertEqual(playedmatch1.score, 5000)
        playedmatch1.user = self.us2
        self.assertEqual(playedmatch1.user, self.us2)
        playedmatch1.game = game2
        self.assertEqual(playedmatch1.game, game2)
    #
    def testSavedGame(self):
        self.us1 = User.objects.create(username="profile1", password="12345678", email="xx@gmail.com")


        game1 = Game.objects.create(title="Clash of Clans", description="No descr", url="http://www.google.com", price=
                                     3, logo="http://www.image.com",
                                    developer=self.us1)
        self.us2 = User.objects.create(username="profile2", password="12345678", email="xxxx@gmail.com")

        game2 = Game.objects.create(title="Fifa 16", description="No descr", url="http://www.yahoo.com", price=
                                    3, logo="http://www.image.com",
                                    developer=self.us2)

        #savedgame1 = GamePlayer.objects.create(status="LOAD", settings="Resolution", user=self.us1, game=game1)
        #the loading is needed



    def testGame(self):
        self.us1 = User.objects.create(username="profile1", password="12345678", email="xx@gmail.com")

        game1 = Game.objects.create(title="Clash of Clans", description="No descr", url="http://www.google.com", price=
                                     3, logo="http://www.image.com",
                                    developer=self.us1)

        game2 = Game.objects.create(title="Fifa 16", description="No descr", url="http://www.yahoo.com", price=
                                        3, logo="http://www.image.com",
                                        developer=self.us1)
        playedmatch1 = GamePlayer.objects.create(user=self.us1, game=game1)
        playedmatch2 = GamePlayer.objects.create(user=self.us1, game=game2)

        # # Test creation
        #self.assertEqual(playedmatch1.game.get(game1.pk), game1)
        

        self.assertEqual(game1.title, "Clash of Clans")
        self.assertEqual(game1.description, "No descr")
        self.assertEqual(game1.url, "http://www.google.com")
        self.assertEqual(game1.price, 3)
        self.assertEqual(game1.logo, "http://www.image.com")
        self.assertEqual(game1.developer, self.us1)

        game1.title = "CC"
        self.assertEqual(game1.title, "CC")
        game1.description = "Hello"
        self.assertEqual(game1.description, "Hello")
        game1.url = "http://www.facebook.com"
        self.assertEqual(game1.url, "http://www.facebook.com")
        game1.price = 7
        self.assertEqual(game1.price, 7)
        game1.logo = "http://www.logonumberone.com"
        self.assertEqual(game1.logo, "http://www.logonumberone.com")


    #  def testTransaction(self):
    #     self.us1 = User.objects.create(username="profile1", password="12345678", email="xx@gmail.com")
    #     game1 = Game.objects.create(title="Clash of Clans", description="No descr", url="http://www.google.com", price=
    #                                  3, logo="http://www.image.com",
    #                                 developer=self.us1)
    #     game2 = Game.objects.create(title="Fifa 16", description="No descr", url="http://www.yahoo.com", price=
    #                                     3, logo="http://www.image.com",
    #                                     developer=self.us1)
    #     playedmatch1 = GamePlayer.objects.create(user=self.us1,game=game2)
    #     transaction1 = Transaction.objects.create(user=self.us1, game=game1,status=1,amount=3)
    #     print(playedmatch1.game)
