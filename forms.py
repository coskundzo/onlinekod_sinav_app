from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', 
                         validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('E-posta', 
                       validators=[DataRequired(), Email()])
    phone_number = StringField('Telefon Numarası', 
                              validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Şifre', 
                           validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifre Tekrar', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt Ol')
