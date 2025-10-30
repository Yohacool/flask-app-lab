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
    return render_template("profile.html", user=user)

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