import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import song_client
from ..forms import SongReviewForm, SearchForm
from ..models import User, Review, Like
from ..utils import current_time

songs = Blueprint("songs", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@songs.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("songs.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@songs.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = song_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@songs.route("/songs/<song_id>", methods=["GET", "POST"])
def song_detail(song_id):
    try:
        result = song_client.get_song_features(song_id)
    except ValueError as e:
        return render_template("song_detail.html", error_msg=str(e))

    form = SongReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=song_id,
            song_title=result.title,
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=song_id)

    return render_template(
        "song_detail.html", form=form, song=result, reviews=reviews
    )
@songs.route("/like/<song_id>", methods=["POST"])
def toggle_liked_song(song_id):
    liked_song = Like(
        commenter=current_user._get_current_object(),
        liked=song_id
    )
    liked_song.save()
    
    return redirect(url_for("songs.song_detail", song_id=song_id))


@songs.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)
    likes = Like.objects(commenter=user)
    img = get_b64_img(user.username)
    return render_template("user_detail.html", user=user, reviews=list(reviews), image=img,likes=list(likes))
    