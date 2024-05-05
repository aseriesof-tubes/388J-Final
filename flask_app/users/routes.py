from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User
import io

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('songs.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, password=hashed)
        user.save()
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('songs.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if(user is not None and 
           bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for('users.account'))
    else:
        flash('authenticate again lil bro')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('songs.index'))

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":

        if update_username_form.submit_username.data and update_username_form.validate():
            new_username = update_username_form.username.data
            current_user.username = new_username
            current_user.save()
            flash('updated')
        else:
            flash('this shit is taken')

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            image = update_profile_pic_form.picture.data
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(image.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(image.stream, content_type=content_type)
            current_user.save()
            flash('updated')

        return redirect(url_for('users.account'))
    
    return render_template('account.html', update_username_form=update_username_form, 
                           update_profile_pic_form=update_profile_pic_form, image=get_b64_img(current_user.username))