from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Index Route Decorator
@app.route('/')
def index():
    return render_template('index.html')


# Error Page Invalid URL
@app.errorhandler(404)
def page_404(e):
    return render_template('errors/404.html'), 404

# Error Page Internal Server Error
@app.errorhandler(500)
def page_500(e):
    return render_template('errors/500.html'), 500

app.run(debug=True)