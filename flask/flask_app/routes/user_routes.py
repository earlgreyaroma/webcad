from . import user_bp
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from ..webforms import UserForm, TestForm
from ..tables import Users, Actions
from .. import db

# Index Route Decorator
@user_bp.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if Users.query.filter_by(admin_check=True).count() == 0:
            return redirect(url_for('admin_bp.admin_setup'))
    elif form.validate_on_submit():
        user = Users.query.filter_by(username=form.user_id.data).first()
        if user and (user.admin_check == False):
            login_user(user)
        else:
            user = Users(username=form.user_id.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        return redirect(url_for('user_bp.part'))
    return render_template('index.html', form=form)

# Part Route Decorator
@user_bp.route('/part', methods=['GET', 'POST'])
@login_required
def part():
    form = TestForm()
    if form.validate_on_submit():
        action = Actions(user_id=current_user.id)
        db.session.add(action)
        db.session.commit()
    return render_template('part.html', form=form)

