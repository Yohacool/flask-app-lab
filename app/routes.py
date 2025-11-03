from flask import request, redirect, url_for, render_template, flash, session, make_response
from .forms import ContactForm
from .forms import LoginForm
from . import app
import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "contacts.log")
contact_logger = logging.getLogger("contact_logger")
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    contact_logger.addHandler(handler)
contact_logger.propagate = False

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template('home.html', agent = agent)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        remember = form.remember.data
        if user == "jar" and password == "1234":
            session['user'] = user
            flash(f"Вітаємо, {user}! {'(Запам’ятати: Так)' if remember else '(Запам’ятати: Ні)'}", "success")
            return redirect(url_for('profile'))
        else:
            flash("Невірні дані для входу. Спробуйте ще раз.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Ви не авторизовані! Увійдіть у систему.", "warning")
        return redirect(url_for("login"))
    user = session["user"]
    cookies = request.cookies.items()
    theme = request.cookies.get("theme", "light")
    return render_template("profile.html", user=session['user'], cookies=cookies, theme=theme)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з акаунту.", "info")
    return redirect(url_for("login"))

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        contact_logger.info(f"Від {name} ({email}, {phone}), тема: {subject} — {message}")
        flash(f"Дякуємо, {name}! Ваше повідомлення успішно надіслано.", "success")
        return redirect(url_for("contacts"))
    elif form.is_submitted():
        flash("Форма заповнена некоректно. Перевірте введені дані.", "danger")
    return render_template("contacts.html", form=form)

@app.route("/add_cookie", methods=["POST"])
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    resp = make_response(redirect(url_for("profile")))
    if key and value:
        resp.set_cookie(key, value, max_age=3600)
        flash(f"Кукі '{key}' додано!", "success")
    else:
        flash("Введіть ключ і значення!", "danger")
    return resp

@app.route("/delete_cookie/<key>")
def delete_cookie(key):
    resp = make_response(redirect(url_for("profile")))
    resp.delete_cookie(key)
    flash(f"Кукі '{key}' видалено!", "info")
    return resp

@app.route("/delete_all_cookies")
def delete_all_cookies():
    resp = make_response(redirect(url_for("profile")))
    for key in request.cookies.keys():
        resp.delete_cookie(key)
    flash("Усі кукі видалено!", "info")
    return resp

@app.route("/set_theme/<color>")
def set_theme(color):
    if color not in ["light", "dark"]:
        flash("Невідома тема!", "warning")
        return redirect(url_for("profile"))

    resp = make_response(redirect(url_for("profile")))
    resp.set_cookie("theme", color, max_age=3600 * 24 * 7)
    flash(f"Тема змінена на {color}.", "success")
    return resp