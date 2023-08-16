"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import datetime, time
import random

from py4web import action,Field, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_username, get_user
from py4web.utils.form import Form, FormStyleBulma

url_signer = URLSigner(session)





@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        get_categories_url = URL("get_categories", signer=url_signer),
        add_category_url = URL("add_category", signer=url_signer),
        get_player_stat_info_url = URL("get_player_stat_info", signer=url_signer),
    )
    
@action('get_player_stat_info', method = ["GET"])
@action.uses(db, auth.user, url_signer)
def get_player_stat_info():
    out = get_user()
    print("\n\nid = ", out, "\n\n")
    return dict(output = out, signer = url_signer)


@action("get_categories")
@action.uses(db, auth.user)
def get_categories():
    # print("getting categories")
    categories = db(db.category).select().as_list()
    temp = db(db.play_data.playerID == get_user()).select().first()
    if temp is None:
        playerData = False
        print("player data not available\n\n")
    else:
        playerData = True
        
    return dict(categories=categories, playerData = playerData)

@action("add_category", method=["GET", "POST"])
@action.uses('add_category.html', db, session, auth.user)
def add_category():
    form = Form(db.category, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL()[:-1])
    return dict(form=form, signer = url_signer)

@action("delete_quiz", method=["POST"])
@action.uses(db, session, auth.user)
def delete_quiz():
    t1 = request.json.get("quizId")
    assert t1 is not None
    temp = db(db.quiz.id == t1).select().first()

    
    if (temp is None) or (int(temp.creatorID) != get_user()):
        return dict()
    
    t2= db(db.category.id == temp.categoryID).select().first()
    t3 = t2.numPuzzles - 1
    t2.update_record(numPuzzles = t3)
    
    db(db.upvote_data.gameId == t1).delete()
    db(db.game_comments.gameId == t1).delete()
    db(db.game_upvotes.game == t1).delete()
    db(db.play_data.quiz == t1).delete()
    
    db(db.quiz.id == t1).delete()
    
    return dict()

@action("edit_quiz/<quizid>", method=['GET','POST'])
@action.uses('add_game.html',db , session, auth.user)
def edit_quz(quizid):
    p=db.quiz[quizid]
    category= db(db.quiz.id == quizid).select().first()
    category=category.categoryName
    form = Form(db.quiz, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('category/'+category))
    return dict(form=form,
                signer=url_signer)
    #form= Form([
    #    Field("gameName", placeholder="What would you like to call your Game?"),
    #    Field("answer", placeholder="Please enter your exact answer"),
    #    Field("image1", placeholder="Please enter a URL link to photo"),
    #    Field("image2", placeholder="Please enter a URL link to photo"),
    #    Field("image3", placeholder="Please enter a URL link to photo"),
    #    Field("image4", placeholder="Please enter a URL link to photo"),
    #    Field("image5", placeholder="Please enter a URL link to photo"),
    #    Field("image6", placeholder="Please enter a URL link to photo"),
    #],formstyle=FormStyleBulma, csrf_session=session)

    #if request.method=="GET":
        #quiz = db(db.quiz.id == quizid).select().first()
     #   quizName = quiz.gameName
      #  answer = quiz.answer
      #  image1 = quiz.image1
      #  image2 = quiz.image2
      #  image3 = quiz.image3
      #  image4 = quiz.image4
      #  image5 = quiz.image5
      #  image6 = quiz.image6
      #  return dict(form=form,
      #              signer=url_signer,
      #              quizName=quizName,
      #              answer=answer,
      #              image1=image1,
      #              image2=image2,
      #              image3=image3,
      #              image4=image4,
      #              image5=image5,
      #              image6=image6)
    #else:
     #   creator=get_user()
        #redirect(URL('category/'+categoryName))


@action("add_game/<categoryName>", method=['GET',"POST"])
@action.uses('add_game.html', db, session, auth.user)
def add_game(categoryName):
    #form = Form(db.quiz, csrf_session=session, formstyle=FormStyleBulma)
    form= Form([
        Field("gameName", placeholder="What would you like to call your Game?"),
        Field("answer", placeholder="Please enter your exact answer"),
        Field("image1", placeholder="Please enter a URL link to photo"),
        Field("image2", placeholder="Please enter a URL link to photo"),
        Field("image3", placeholder="Please enter a URL link to photo"),
        Field("image4", placeholder="Please enter a URL link to photo"),
        Field("image5", placeholder="Please enter a URL link to photo"),
        Field("image6", placeholder="Please enter a URL link to photo"),
    ],formstyle=FormStyleBulma, csrf_session=session)
    if request.method=="GET":
        print(categoryName)
    else:
        catID= db(db.category.categoryName==categoryName).select().first().id
        creator=get_user()
        print(catID)
        print(creator)
        db.quiz.insert(categoryName=categoryName, image1=form.vars["image1"],image2=form.vars["image2"],
                       image3=form.vars["image3"],image4=form.vars["image4"], image5=form.vars["image5"],
                       image6=form.vars["image6"],answer=form.vars["answer"],gameName=form.vars["gameName"],
                       categoryID=catID,creatorID=creator)
        temp = db(db.category.id == catID).select().first().numPuzzles
        db(db.category.id== catID).update(numPuzzles = temp + 1)
        redirect(URL('category/'+categoryName))
    return dict(form=form, signer = url_signer)



@action("game_state_update", method=["POST"])
@action.uses(db, auth.user, session)
def game_state_update():
    tryNum = request.json.get('tryNum')
    guess = request.json.get('guess')
    answer = request.json.get('answer')
    quizId = request.json.get('quizId')
    status = (guess == answer)
    temp = db((db.play_data.playerID == get_user()) & (db.play_data.quiz == quizId)).select().first()
    gameResult = 0
    if status:
        gameResult = 1
        if temp is None:
            db.play_data.insert(playerID = get_user(), status = gameResult, guesses = tryNum, quiz = quizId)
        else:
            db(db.play_data.id == temp.id).update(status = gameResult, guesses = tryNum)
        
        
    else:
        tryNum = tryNum + 1
        if tryNum > 6:
            gameResult = -1
        if temp is None:
            db.play_data.insert(playerID = get_user(), status = gameResult, guesses = tryNum, quiz = quizId)
        else:
            db(db.play_data.id == temp.id).update(status = gameResult, guesses = tryNum)
    return dict(status = gameResult, tryNum = tryNum)


@action("stats/<playerID>")
@action.uses("stat_display.html", db, auth.user, session, url_signer)
def stat_display(playerID):
    return dict(
        playerID = playerID,
        player_stats_load_url = URL("player_stats_load", signer=url_signer),
        load_users_url= URL("load_users", signer=url_signer)
    )
    


@action("player_stats_load", method=["GET"])
@action.uses( db, auth.user, session, url_signer)
def player_stats_load():
    pi = request.params.get("playerId")
    out2 = db(db.auth_user.id == pi).select().first().username
    out1 = db(db.play_data.playerID == pi).select(orderby=~db.play_data.id)
    print("\n\nout1 = ", out1, "   end\n\n")
    
    for row in out1:
        qn = db(db.quiz.id == row.quiz).select(db.quiz.gameName).first().gameName
        qn = qn + "     |  Id= " + str(row.quiz)
        row.quiz = qn
    return dict(gamedata = out1, uname = out2)


@action("category/<categoryName>", method=["GET", "POST"])
@action.uses("quiz_selection.html", db, auth.user, session, url_signer)
def quizzes(categoryName):    
    return dict(
        categoryName = categoryName,
        get_quizzes_url = URL("get_quizzes", signer=url_signer),
        delete_quiz_url = URL("delete_quiz", signer=url_signer),
        )


# gets all quizzes belonging in a certain category
@action("get_quizzes")
@action.uses(db, auth.user, session)
def get_quizzes():
    categoryName = request.params.get('categoryName')
    assert categoryName is not None

    #TODO if categoryName == "AllCategories" ..., select all quizzes

    quizzes = db(db.quiz['categoryName'] == categoryName).select().as_list()
    temp = db((db.quiz.creatorID == get_user) & (db.quiz.categoryName == categoryName)).select(db.quiz.id)
    owned = [row.id for row in temp]
    print("\n\nowned = ", owned, "\n\n")
    return dict(quizzes = quizzes, owned = owned)

@action("get_answers")
@action.uses(db, auth.user, session)
def get_answers():
    answers = []
    qi = request.params.get('qid')
    print("\n\nqi = ", qi, "    end\n\n")
    assert qi is not None
    q = db(db.quiz.id == qi).select().first()
    print("q = ", "\n\n")
    for row in db(db.quiz.categoryName == q.categoryName).select(db.quiz.answer):
        if (row["answer"] not in answers):
            answers.append(row["answer"])
    return dict(answers=answers)

@action("quiz/<quiz_id>", method=["GET", "POST"])
@action.uses("quiz_play.html", db, auth.user, session, url_signer)
def quiz_play(quiz_id):
    return dict(
        quiz_id=quiz_id,
        get_quiz=URL('get_quiz'),
        get_comments_url = URL('get_comments'),
        comment_upvote_process_url = URL('comment_upvote_process'),
        comment_post_process_url = URL('comment_post_process'),
        delete_comment_url = URL('delete_comment'),
        game_upvote_process_url = URL('game_upvote_process'),
        get_answers_url = URL('get_answers'),
        game_state_update_url = URL('game_state_update'),
        )

@action("jump_to_play")
@action.uses("quiz_play.html")
def jump_to_play():
    return dict(get_quiz=URL('get_quiz'))


@action("get_quiz", method=["POST"])
@action.uses(db, auth.user, session)
def get_quiz():
    quiz_id=request.json.get("quiz_id")
    quiz=db(db.quiz.id==quiz_id).select()
    user = get_user()
    gameUpvoteStatus = db((db.game_upvotes.user == user) & (db.game_upvotes.game == quiz_id)).select().first()
    print("\n\ngameUpvoteStatus = ", gameUpvoteStatus, "\n\n")
    if gameUpvoteStatus is None:
        gus = 0
    else:
        gus = gameUpvoteStatus.status
    playdata = db((db.play_data.playerID == get_user()) & (db.play_data.quiz == quiz_id)).select().first()
    print("\n\nplaydata = ", playdata, "   end\n\n")
    
    return dict(quiz=quiz, gameUpvoteStatus = gus, playdata = playdata)

@action("comment_post_process", method=["POST"])
@action.uses(db, auth.user, session)
def comment_post_process():
    # print("\n\nReached\n\n")
    user = get_username()
    post = request.json.get("post")
    gameId = request.json.get("gameId")
    db.game_comments.insert(author = user, gameId = gameId, likeRatio = 0,
                            postBody = post, time = datetime.datetime.now().isoformat())
    db.commit()
    
    return dict()

@action("delete_comment", method=["POST"])
@action.uses(db, auth.user, session)
def delete_comment():
    postId = request.json.get('postId')
    uinfo = db(db.upvote_data.post == postId).select()
    for post in uinfo:
        post.delete_record()
    temp = db(db.game_comments.id == postId).select()
    for post in temp:
        post.delete_record()
    return dict()

@action("get_comments", method=["GET"])
@action.uses(db, auth.user, session)
def get_comments():
    # print("\n\nget comments claled in python\n")
    gameId = request.params.get('gameId')
    # print("\n\gameId = ")
    # print(gameId)
    # print("\n\n")
    user = db(db.auth_user.username == get_username()).select().first()
    # print("\n\nuser.id = ")
    # print(user)
    # print("\n\n")
    # test1=db(db.game_comments).select()
    # print("\ntest1 = ", test1, "\n\n")
    output = db(db.game_comments.gameId == gameId).select()
    u1= db((db.upvote_data.gameId == gameId) &
                   (db.upvote_data.user == user.id)).select()
    upvoteData = [u2.post for u2 in u1]
    upvoteStatus = [u2.status for u2 in u1]
    cu = get_username()
    ownerStatus = [(i.author == cu) for i in output]
    print("\n\nownerstatus = ", ownerStatus, "\n\n")
    # print("\n\noutput = ")
    # print(output)
    # print("\n\n")
    # print("upvotedata = ", upvoteData, "\n\n")
    
    return dict(output = output, upvoteData = upvoteData, 
                upvoteStatus = upvoteStatus, ownerStatus = ownerStatus)

@action("comment_upvote_process", method=["POST"])
@action.uses(db, auth.user, session)
def comment_upvote_process():
    upvote = request.json.get("upvote")
    post = request.json.get("post")
    user = get_user()
    
    placeholder = db((db.upvote_data.post == post) & (db.upvote_data.user == user)).select().first()
    
    total = db(db.game_comments.id == post).select().first().likeRatio
    
    # print("\n\nplaceholder = ", placeholder, "\n")
    
    if placeholder is None:
        gameId = (db(db.game_comments.id == post).select().first()).id
        db.upvote_data.insert(user = user,
                           post = post, status = upvote, gameId = gameId)
        total = total + upvote
        db(db.game_comments.id == post).update(likeRatio = total)
        return dict(total = total)
    
    
    if upvote == placeholder.status:
        db(db.upvote_data.id == placeholder.id).delete()
        total = total - upvote
        db(db.game_comments.id == post).update(likeRatio = total)
        return dict(total = total)
    
    total = total + (upvote * 2)
    db(db.upvote_data.id == placeholder.id).update(status = upvote)
    db(db.game_comments.id == post).update(likeRatio = total)
    
    
    return dict(total = total)

@action("game_upvote_process", method=["POST"])
@action.uses(db, auth.user, session)
def game_upvote_process():
    print("\n\ngame upvote called\n\n\n")
    order = request.json.get("order")
    
    game = request.json.get("game")
    user = get_user()
    
    temp = db(db.quiz.id == game).select().first()
    print("\n\ntemp =", temp, "\n\n")
    print("\n\ntemp.downvotes = ", temp.upvotes, "\n\n")
    print("\n\ntemp.upvotes = ", temp.upvotes, "\n\n")
    
    
    placeholder = db((db.game_upvotes.game == game) & (db.game_upvotes.user == user)).select().first()
    
    if placeholder is None:
        db.game_upvotes.insert(user = user, game = game, status = order)
        if order > 0:
            upvotes =  temp.upvotes + 1
            downvotes = temp.downvotes
            db(db.quiz.id == game).update(upvotes = upvotes)
        else:
            downvotes = temp.downvotes + 1
            upvotes = temp.upvotes
            db(db.quiz.id == game).update(downvotes = downvotes)
        status = order
    else:
        print("\norder = ", order, "\n\n")
        print("\nplaceholder.status = ", placeholder.status, "\n\n")
        if placeholder.status == order:
            if order == 1:
                downvotes = temp.downvotes
                upvotes = temp.upvotes - 1
                db(db.quiz.id == game).update(upvotes = upvotes)
            else:
                upvotes = temp.upvotes
                downvotes = temp.downvotes - 1
                db(db.quiz.id == game).update(downvotes = downvotes)
            status = 0
            db((db.game_upvotes.game == game) & (db.game_upvotes.user == user)).select().first().delete_record()
        else:
            if order == 1:
                upvotes = temp.upvotes + 1
                downvotes = temp.downvotes - 1
                db(db.quiz.id == game).update(upvotes = upvotes, downvotes = downvotes)
            else:
                upvotes = temp.upvotes - 1
                downvotes = temp.downvotes + 1
                db(db.quiz.id == game).update(upvotes = upvotes, downvotes = downvotes)
            status = order
            db(db.game_upvotes.id == placeholder.id).update(status = status)
    return dict(upvotes = upvotes, downvotes = downvotes, status = status)


@action("load_users", method=["GET"])
@action.uses(db, auth.user, session)
def load_users():
    t1 = db(db.auth_user.id == db.play_data.playerID).select(db.auth_user.id, 
                                                    db.auth_user.username, distinct=True)
    print("called\n")
    return dict(output = t1)