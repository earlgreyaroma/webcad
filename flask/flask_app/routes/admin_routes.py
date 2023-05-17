from . import admin_bp
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from ..webforms import AdminForm, AdminRegisterForm, KeysForm
from ..tables import Users, API_Keys
from .. import db, osc

# Admin Route Decorator
@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_index():
    if current_user.is_authenticated and (current_user.admin_check == True):
        return redirect(url_for('admin_bp.admin_settings'))
    else:
        form = AdminForm()
        if Users.query.filter_by(admin_check=True).count() == 0:
            return redirect(url_for('admin_bp.admin_setup'))
        elif form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user and (user.admin_check == True):
                if user.verify_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('admin_bp.admin_settings'))
            form.username.data = ''
            form.password.data = ''
        return render_template('admin/index.html', form=form)

# Admin First Login Route Decorator
@admin_bp.route('/admin/setup', methods=['GET', 'POST'])
def admin_setup():
    if Users.query.filter_by(admin_check=True).count() != 0:
        return redirect(url_for('admin_bp.admin_index'))
    else:
        form = AdminRegisterForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None:
                user = Users(admin_check=True, username=form.username.data)
                user.password = form.password.data 
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('admin_bp.admin_index'))
            form.username.data = ''
            form.password.data = ''
            form.password2.data = ''
        return render_template('admin/setup.html', form=form)

# Admin Settings Route Decorator
@admin_bp.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if current_user.admin_check == True:
        if API_Keys.query.count() == 0:
            return redirect(url_for('admin_bp.admin_keys'))
        else:
            api_keys = API_Keys.query.filter_by(user_id=current_user.id).order_by(API_Keys.date_added.desc()).first
        return render_template('admin/settings.html')
    else:
        return redirect(url_for('admin_bp.admin_index'))

# Admin Logout Route Decorator
@admin_bp.route('/admin/logout', methods=['GET', 'POST'])
@login_required
def admin_logout():
    if current_user.admin_check == True:
        logout_user()
    return redirect(url_for('admin_bp.admin_index'))

# Admin API Keys Route Decorator
@admin_bp.route('/admin/settings/keys/update', methods=['GET', 'POST'])
@login_required
def admin_keys():
    if current_user.admin_check == True:
        form = KeysForm()
        if form.validate_on_submit():
            new_keys = API_Keys(user_id=current_user.id, access_key=form.access_key.data, secret_key=form.secret_key.data)
            db.session.add(new_keys)
            db.session.commit()
            osc.auth(new_keys.access_key, new_keys.secret_key)
            return redirect(url_for('admin_bp.admin_settings'))
        return render_template('admin/keys.html', form=form)
    else:
        return redirect(url_for('admin_bp.admin_index'))
