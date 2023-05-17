from . import error_bp
from flask import render_template

# Error Page Invalid URL
@error_bp.errorhandler(404)
def page_404(e):
    return render_template('errors/404.html'), 404

# Error Page Internal Server Error
@error_bp.errorhandler(500)
def page_500(e):
    return render_template('errors/500.html'), 500

