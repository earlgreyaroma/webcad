from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super duper secret key'

# Initialize MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db/mydatabase'
db = SQLAlchemy(app)

# Create MySQL Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(255), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Create Form Class
class UserForm(FlaskForm):
    userID = StringField(validators=[DataRequired()])
    submit = SubmitField('Start')

# Index Route Decorator
@app.route('/', methods=['GET', 'POST'])
def index():
    userID = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(userID=form.userID.data).first()
        if user is None:
            user = Users(userID=form.userID.data)
            db.session.add(user)
            db.session.commit()
        userID = form.userID.data
        form.userID.data = ''
        return redirect(url_for('part', userID=userID))
    return render_template('index.html', form=form)

# Part Route Decorator
@app.route('/part/<userID>')
def part(userID):
    return render_template('part.html', userID=userID)


# Error Page Invalid URL
@app.errorhandler(404)
def page_404(e):
    return render_template('errors/404.html'), 404

# Error Page Internal Server Error
@app.errorhandler(500)
def page_500(e):
    return render_template('errors/500.html'), 500

app.run(debug=True)