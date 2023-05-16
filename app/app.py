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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@10.0.0.2:5432/mydatabase'
db = SQLAlchemy(app)

# Create MySQL Model
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Create Form Class
class UserForm(FlaskForm):
    user_id = StringField(validators=[DataRequired()])
    submit = SubmitField('Start')

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
        user_id = form.user_id.data
        form.user_id.data = ''
        return redirect(url_for('part', user_id=user_id))
    return render_template('index.html', form=form)

# Part Route Decorator
@app.route('/part/<user_id>')
def part(user_id):
    return render_template('part.html', user_id=user_id)


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