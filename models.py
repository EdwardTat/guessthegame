"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later







db.define_table(
    "category",
    Field("categoryName", type='string'),
    Field("numPuzzles", 'integer', readable=False, writable=False, default=0),
    Field("numViews", readable=False, writable=False, default=0),
)



db.define_table(
    "quiz",
    Field("gameName"),
    Field("answer"),
    Field("categoryName", readable=False,writable=False, hidden=True),
    Field("categoryID", "reference category", readable=False, writable=False, hidden=True),
    # https://nicozanf.github.io/py4web-doc/en/master/chapter-07.html#more-on-uploads
    Field("image1"),
    Field("image2"),
    Field("image3"),
    Field("image4"),
    Field("image5"),
    Field("image6"),
    Field("creatorID", readable=False, writable=False , hidden=True),
    Field("upvotes", 'integer', readable=False,writable=False, hidden=True,  default='0'),
    Field("downvotes", 'integer', readable=False,writable=False, hidden=True, default='0'),
)

db.define_table('game_comments',
    Field('author'),
    Field('gameId', 'reference quiz'),
    Field('likeRatio', 'integer'),
    Field('postBody'),
    Field('time')
)

db.define_table('upvote_data',
    Field('user', 'reference auth_user'),
    Field('post', 'reference game_comments'),
    Field('status', 'integer'),
    Field('gameId', 'reference quiz'),
)


db.define_table('game_upvotes',
    Field('user', 'reference auth_user'),
    Field('game', 'reference quiz'),
    Field('status', 'integer'),
)



db.define_table('play_data',
    Field('playerID', 'reference auth_user'),
    Field('status'),
    Field('guesses', 'integer'),
    Field('quiz', 'reference quiz'),
)

def add_example_categories():
    db.category.truncate()
    db.quiz.truncate()
    for i in range(5):
        name = "example" + str(i)
        numPuzzles = i
        numViews = i
        c = dict(
            id = i,
            categoryName = name,
            numPuzzles = numPuzzles,
            numViews = numViews,
        )
        db.category.insert(**c)

        for i in range(5):
            image = "https://cdn.discordapp.com/attachments/1114810706299195453/1114810967822434345/IMG_6127.jpg"
            q = dict(
                categoryName = name,
                image1=image,
                image2="https://cdn.discordapp.com/attachments/1114810706299195453/1114810968296403014/IMG_6128.jpg",
                image3="https://cdn.discordapp.com/attachments/1114810706299195453/1114810968741007420/IMG_6129.jpg",
                image4="https://cdn.discordapp.com/attachments/1114810706299195453/1114810969244315668/IMG_6130.jpg",
                image5="https://cdn.discordapp.com/attachments/1114810706299195453/1114810969646977035/IMG_6131.jpg",
                image6="https://cdn.discordapp.com/attachments/1114810706299195453/1114811175331430470/IMG_6132.jpg",
                gameName="edward",
                creatorID=i,
                answer="edward"
            )

        db.quiz.insert(**q)
        image = "https://cdn.discordapp.com/attachments/1114810706299195453/1114810967822434345/IMG_6127.jpg"
        q = dict(
            categoryName = name,
            image1=image,
            image2="https://cdn.discordapp.com/attachments/1114810706299195453/1114810968296403014/IMG_6128.jpg",
            image3="https://cdn.discordapp.com/attachments/1114810706299195453/1114810968741007420/IMG_6129.jpg",
            image4="https://cdn.discordapp.com/attachments/1114810706299195453/1114810969244315668/IMG_6130.jpg",
            image5="https://cdn.discordapp.com/attachments/1114810706299195453/1114810969646977035/IMG_6131.jpg",
            image6="https://cdn.discordapp.com/attachments/1114810706299195453/1114811175331430470/IMG_6132.jpg",
            gameName="edward",
            creatorID=i,
            answer="notedward"
        )
        db.quiz.insert(**q)


        image = "https://cdn.discordapp.com/attachments/1114810706299195453/1114810967822434345/IMG_6127.jpg"
        q = dict(
            categoryName = name,
            image1=image,
            image2="https://cdn.discordapp.com/attachments/1114810706299195453/1114810968296403014/IMG_6128.jpg",
            image3="https://cdn.discordapp.com/attachments/1114810706299195453/1114810968741007420/IMG_6129.jpg",
            image4="https://cdn.discordapp.com/attachments/1114810706299195453/1114810969244315668/IMG_6130.jpg",
            image5="https://cdn.discordapp.com/attachments/1114810706299195453/1114810969646977035/IMG_6131.jpg",
            image6="https://cdn.discordapp.com/attachments/1114810706299195453/1114811175331430470/IMG_6132.jpg",
            gameName="edward",
            creatorID=i,
            answer="answer1"
        )
        db.quiz.insert(**q)


db.commit()





