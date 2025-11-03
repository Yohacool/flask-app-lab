from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(message="Введіть ім'я"),
            Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email"),
            Email(message="Некоректний email")
        ]
    )
    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Введіть номер телефону"),
            Regexp(r'^\+380\d{9}$', message="Формат телефону має бути +380XXXXXXXXX")
        ]
    )
    subject = SelectField(
        "Тема",
        choices=[
            ("support", "Підтримка"),
            ("feedback", "Відгук"),
            ("advertising", "Реклама"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть повідомлення"),
            Length(max=500)
        ]
    )
    submit = SubmitField("Надіслати")

class LoginForm(FlaskForm):
    user = StringField("Ім'я користувача або Email", validators=[DataRequired(message="Поле обов'язкове")])
    password = PasswordField("Пароль", validators=[
        DataRequired(message="Поле обов'язкове"),
        Length(min=4, max=10, message="Довжина паролю від 4 до 10 символів")
    ])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")