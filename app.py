from flask import Flask
from config import Config
from extensions import db, login_manager, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Lütfen giriş yapınız.'
    
    # Import models
    from models import User, Question, ExamAttempt, Answer
    
    # Register user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp, init_oauth
    from routes.exam import exam_bp
    from routes.main import main_bp
    from routes.admin import admin_bp
    
    # Initialize OAuth
    init_oauth(app)
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(exam_bp, url_prefix='/exam')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
