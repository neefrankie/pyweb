from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4
from tuzhi.forms import SignUpForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()

    if form.validate_on_submit():
        print(form.data)
        pw_hash = generate_password_hash(form.password.data)
        print(pw_hash)
        session.clear()
        session['user_id'] = uuid4()
        return redirect(url_for('index'))
    
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session.clear()
        session['user_id'] = uuid4()
        return redirect(url_for('index'))

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
