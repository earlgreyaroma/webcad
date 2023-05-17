from . import user_bp
from flask import render_template, redirect, url_for
from ..webforms import UserForm, TestForm
from ..tables import Users, Interactions
from .. import db

# Index Route Decorator
@user_bp.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(user_id=form.user_id.data).first()
        if user:
            pass
            #login_user(user)
        else:
            user = Users(user_id=form.user_id.data)
            db.session.add(user)
            db.session.commit()
            #login_user(user)
        return redirect(url_for('user_bp.part', user_id=user.id))
    return render_template('index.html', form=form)

# Part Route Decorator
@user_bp.route('/part/<user_id>', methods=['GET', 'POST'])
def part(user_id):
    form = TestForm()
    if form.validate_on_submit():
        interaction = Interactions(user_table_id=user_id)
        db.session.add(interaction)
        db.session.commit()
    return render_template('part.html', form=form)

