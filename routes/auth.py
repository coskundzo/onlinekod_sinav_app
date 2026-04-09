from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from authlib.integrations.flask_client import OAuth
from models import User
from extensions import db
from forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

# Initialize OAuth
oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth with app config"""
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Kullanıcı adı veya e-posta zaten kullanılıyor.', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone_number=form.phone_number.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Hoş geldin, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Geçersiz kullanıcı adı veya şifre.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/google-login')
def google_login():
    """Redirect to Google OAuth"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/google-callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')

        # Fallback for cases where provider response doesn't include userinfo inline.
        if not user_info:
            user_info_response = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo')
            user_info = user_info_response.json() if user_info_response else None
        
        if not user_info or not user_info.get('sub') or not user_info.get('email'):
            flash('Google girişi başarısız oldu.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Check if user exists
        user = User.query.filter_by(google_id=user_info['sub']).first()
        
        if not user:
            # Check if email already exists
            user = User.query.filter_by(email=user_info['email']).first()
            
            if user:
                # Link Google account to existing user
                user.google_id = user_info['sub']
                db.session.commit()
                flash('Google hesabınız mevcut hesabınıza bağlandı.', 'success')
            else:
                # Create new user
                username = user_info['email'].split('@')[0]
                # Make username unique if it already exists
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=user_info['email'],
                    google_id=user_info['sub'],
                    phone_number=None  # Phone will be asked later if needed
                )
                db.session.add(user)
                db.session.commit()
                flash('Google hesabınızla başarıyla kayıt oldunuz!', 'success')
        
        # Log the user in
        login_user(user, remember=True)
        flash(f'Hoş geldin, {user.username}!', 'success')
        return redirect(url_for('main.dashboard'))
        
    except Exception as e:
        flash(f'Google girişi sırasında bir hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))
