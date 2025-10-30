from flask import request, redirect, url_for, render_template, abort, flash, session, make_response
from . import app

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
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "jar" and password == "123":
            session["user"] = username
            flash("Вхід виконано успішно!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Невірний логін або пароль!", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Ви не авторизовані! Увійдіть у систему.", "warning")
        return redirect(url_for("login"))
    user = session["user"]
    cookies = request.cookies.items()
    theme = request.cookies.get("theme", "light")
    return render_template("profile.html", user=user, cookies=cookies, theme=theme)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з акаунту.", "info")
    return redirect(url_for("login"))

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

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