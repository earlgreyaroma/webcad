from . import user_bp
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from ..tables import Users, Actions, API_Keys
from .. import db, osc
from onshapeclient import Client

user_osc = Client()

# Index Route Decorator
@user_bp.route('/', methods=['GET', 'POST'])
def index():
    if (Users.query.filter_by(admin_check=True).count() == 0) or (API_Keys.query.count() == 0):
        return redirect(url_for('admin_bp.create'))
    elif request.method == 'POST':
        username = request.form.get('username')
        user = Users.query.filter_by(username=username).first()

        if user is None:
            user = Users(username=username)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        elif user and (user.admin_check == False):
            login_user(user)
        return redirect(url_for('user_bp.part'))
    
    return render_template('index.html')

# Part Route Decorator
@user_bp.route('/part', methods=['GET', 'POST'])
@login_required
def part():
    api_keys = API_Keys.query.order_by(API_Keys.id.desc()).first()
    user_osc.auth(api_keys.access_key, api_keys.secret_key)
    [did, wid] = osc.copy_workspace(current_user.id)
    user_osc.set_did(did)
    user_osc.set_wid(wid)
    eids = user_osc.get_eids()
    for key, value in eids.items():
        if key == osc.eid_name:
            eid = value
        elif key == osc.veid_name:
            veid = value
    user_osc.set_eid(eid)
    user_osc.set_veid(veid)
    return render_template('part.html')

# Part Route Decorator
@user_bp.route('/get_gltf', methods=['GET'])
@login_required
def get_gltf():
    gltf = user_osc.get_gltf()
    return jsonify(gltf)

# Part Route Decorator
@user_bp.route('/process_var', methods=['POST'])
@login_required
def process_var():
    data = request.get_json()
    var = data['var']
    value = data['value']
    #user_osc.change_varstudio_var(var, value)
    return jsonify(data)
