from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super duper secret key'

# Initialize MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@10.0.0.2:5432/mydatabase'
db = SQLAlchemy(app)

# setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_index'

@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))

# Create MySQL Model
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(255), nullable=False, unique=True)

# Create MySQL Model
class Interactions(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(255), nullable=False, unique=True)
    
# Create MySQL Model
class Admins(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# Create User Form Class
class UserForm(FlaskForm):
    user_id = StringField(validators=[DataRequired()])
    submit = SubmitField('Start')

# Create Admin Form Class
class AdminForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')

# Create Admin Form Class
class AdminRegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), EqualTo('password2', message='Passwords Must Match!')])
    password2 = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Register')

# Index Route Decorator
@app.route('/', methods=['GET', 'POST'])
def index():
    user_id = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(user_id=form.user_id.data).first()
        if user is None:
            user = Users(user_id=form.user_id.data)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('part', user_id=user.iser_id))
    return render_template('index.html', form=form)

# Part Route Decorator
@app.route('/part/<user_id>')
def part(user_id):
    return render_template('part.html', user_id=user_id)

# Admin Route Decorator
@app.route('/admin', methods=['GET', 'POST'])
def admin_index():
    form = AdminForm()
    if form.validate_on_submit():
        user = Admins.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('admin_settings'))
        form.username.data = ''
        form.password.data = ''
    return render_template('admin/index.html', form=form)

# Admin First Login Route Decorator
@app.route('/admin/setup', methods=['GET', 'POST'])
def admin_setup():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        user = Admins.query.filter_by(username=form.username.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password.data, method='scrypt')
            user = Admins(username=form.username.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        form.username.data = ''
        form.password.data = ''
        form.password2.data = ''
    return render_template('admin/setup.html', form=form)

# Admin Settings Route Decorator
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    return render_template('admin/settings.html')

# Admin Logout Route Decorator
@app.route('/admin/logout', methods=['GET', 'POST'])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_index'))

# Error Page Invalid URL
@app.errorhandler(404)
def page_404(e):
    return render_template('errors/404.html'), 404

# Error Page Internal Server Error
@app.errorhandler(500)
def page_500(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)