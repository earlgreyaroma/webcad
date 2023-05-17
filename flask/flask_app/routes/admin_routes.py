from . import admin_bp
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from ..webforms import AdminForm, AdminRegisterForm, KeysForm
from ..tables import Admins
from .. import db

# Admin Route Decorator
@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_index():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.admin_settings'))
    else:
        form = AdminForm()
        if Admins.query.count() == 0:
            return redirect(url_for('admin_bp.admin_setup'))
        elif form.validate_on_submit():
            user = Admins.query.filter_by(username=form.username.data).first()
            if user:
                if user.verify_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('admin_bp.admin_settings'))
            form.username.data = ''
            form.password.data = ''
        return render_template('admin/index.html', form=form)

# Admin First Login Route Decorator
@admin_bp.route('/admin/setup', methods=['GET', 'POST'])
def admin_setup():
    if Admins.query.count() != 0:
        return redirect(url_for('admin_bp.admin_index'))
    else:
        form = AdminRegisterForm()
        if form.validate_on_submit():
            user = Admins.query.filter_by(username=form.username.data).first()
            if user is None:
                user = Admins(username=form.username.data)
                user.password = form.password.data 
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('admin_bp.admin_index'))
            form.username.data = ''
            form.password.data = ''
            form.password2.data = ''
        return render_template('admin/setup.html', form=form)

# Admin Settings Route Decorator
@admin_bp.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    user = current_user
    if user.access_key is None:
        return redirect(url_for('admin_bp.admin_keys'))
    return render_template('admin/settings.html')

# Admin Logout Route Decorator
@admin_bp.route('/admin/logout', methods=['GET', 'POST'])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_bp.admin_index'))

# Admin API Keys Route Decorator
@admin_bp.route('/admin/settings/keys/update', methods=['GET', 'POST'])
@login_required
def admin_keys():
    user = current_user
    key_form = KeysForm()
    if key_form.validate_on_submit():
        current_user.access_key = key_form.access_key.data
        current_user.secret_key = key_form.secret_key.data
        db.session.commit()
        return redirect(url_for('admin_bp.admin_settings'))
    return render_template('admin/keys.html', key_form=key_form)
