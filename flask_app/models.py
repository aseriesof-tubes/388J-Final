from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager

# Don't need to touch
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField()
    profile_pic = db.ImageField(required=False)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Like(db.Document):
    commenter = db.ReferenceField('User')
    liked = db.StringField()

class Review(db.Document):
    commenter = db.ReferenceField('User')
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    imdb_id = db.StringField(required=True, length=9)
    song_title = db.StringField(required=True, min_length=1, max_length=100)
    image = db.StringField()
