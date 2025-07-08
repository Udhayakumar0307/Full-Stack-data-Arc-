from flask import Flask ,  render_template
from app.auth.routes import auth_bp
from app.users.routes import users_bp
from app.projects.routes import projects_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = '0307UkDaHm'
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)

    @app.route('/')
    def home():
      return render_template('index.html')


    return app
