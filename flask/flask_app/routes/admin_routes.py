from . import admin_bp
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from ..webforms import AdminForm, AdminRegisterForm, KeysForm, DidForm, EidForm
from ..tables import Users, API_Keys
from .. import db, osc
import base64


# Admin Route Decorator
@admin_bp.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated and (current_user.admin_check == True):
        return redirect(url_for('admin_bp.settings'))
    else:
        form = AdminForm()
        if Users.query.filter_by(admin_check=True).count() == 0:
            return redirect(url_for('admin_bp.create'))
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
@admin_bp.route('/create', methods=['GET', 'POST'])
def create():
    if Users.query.filter_by(admin_check=True).count() != 0:
        return redirect(url_for('admin_bp.index'))
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            password_check = request.form.get('passwordCheck')

            if username is None or password is None or password_check is None:
                return "Invalid username or password", 400
            elif password != password_check:
                return "Passwords do not match", 400
            else:
                user = Users.query.filter_by(username=username).first()
                if user:
                    return "Username already exists", 400
                else:
                    user = Users(admin_check=True, username=username)
                    user.password = password
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('admin_bp.index'))

        return render_template('admin/create.html')

# Admin Logout Route Decorator
@admin_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def admin_logout():
    if current_user.admin_check == True:
        logout_user()
    return redirect(url_for('admin_bp.admin_index'))


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.admin_check:
        api_keys = API_Keys.query.filter_by(user_id=current_user.id).first()
        dids = None
        if api_keys:
            access_key = api_keys.access_key
            secret_key = api_keys.secret_key
        return render_template('admin/settings.html', api_keys=api_keys)
    else:
        return redirect(url_for('user_bp.index'))

@admin_bp.route('/settings/process_keys', methods=['POST'])
@login_required
def process_keys():
    if current_user.admin_check:
        access_key = request.form.get('access-key')
        secret_key = request.form.get('secret-key')
        check = osc.auth(access_key, secret_key)
        user_keys = API_Keys.query.filter_by(user_id=current_user.id).first()
        if check and (user_keys is None):
            new_keys = API_Keys(user_id=current_user.id, access_key=access_key, secret_key=secret_key)
            db.session.add(new_keys)
            db.session.commit()
        elif check:
            user_keys.access_key = access_key
            user_keys.secret_key = secret_key
            db.session.commit()
    return redirect(url_for('admin_bp.settings'))

# Admin First Login Route Decorator
@admin_bp.route('/settings/process_did', methods=['POST'])
@login_required
def process_did():
    if current_user.admin_check:
        data = request.get_json()
        did = data['did']
        osc.set_did(did)
        wid = osc.get_wid()
        osc.set_wid(wid)
        all_eids = osc.get_eids()
        eids = {key: value for key, value in all_eids.items() if key.startswith("Part") or key.startswith("Assembly")}
        veids = {key: value for key, value in all_eids.items() if key.startswith("Variable")}
        response_data = [eids, veids]
        return jsonify(response_data)

# Admin First Login Route Decorator
@admin_bp.route('/settings/get_dids', methods=['GET'])
@login_required
def get_dids():
    if current_user.admin_check:
        dids = osc.get_dids()
        return jsonify(dids)


# Admin First Login Route Decorator
@admin_bp.route('/settings/process_eid', methods=['POST'])
@login_required
def process_eid():
    if current_user.admin_check:
        data = request.get_json()
        eid = data['eid']
        eid_name = data['eid_name']
        osc.set_eid(eid)
        osc.set_eid_name(eid_name)
        thumbnail_bin = osc.get_thumbnail('300x300')
        thumbnail_base64 = base64.b64encode(thumbnail_bin).decode('utf-8')
        return thumbnail_base64


# Admin First Login Route Decorator
@admin_bp.route('/settings/process_veid', methods=['POST'])
@login_required
def process_veid():
    if current_user.admin_check:
        data = request.get_json()
        veid = data['veid']
        veid_name = data['veid_name']
        osc.set_veid(veid)
        osc.set_veid_name(veid_name)
        _vars = osc.get_variables_dict()
        return jsonify(_vars)

# Admin First Login Route Decorator
@admin_bp.route('/settings/process_range', methods=['POST'])
@login_required
def process_range():
    if current_user.admin_check:
        data = request.get_json()
        range_param = data['parameter']
        range_value = data['value']
        range_min = data['min']
        range_max = data['max']
        range_steps = data['steps']
        if range_max and range_min and range_steps and range_param and range_value:
            return jsonify(data)
        else:
            return jsonify(result=False)





