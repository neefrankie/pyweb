import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    session,
    url_for,
)

from flaskr.db import db
from flaskr.forms import SignUpForm, LoginForm
from flaskr.models import User

# A Blueprint is a way to organize a group of related views and other code.
# Rather than registering views and other code directly with an application,
# they are registered with a blueprint. Then the blueprint is registered with
# the application when it is available in the factory function.
bp = Blueprint('auth', __name__, url_prefix='/auth')


# This creates a Blueprint named 'auth'. Like the application object,
# the blueprint needs to know where it's defined, so __name__ is passed
# as the second argument. The url_prefix will be prepended to all the
# URLs associated with the blueprint.


# `@bp.route` associates the URL `/register` with the `register` view
# function. When Flask receives a request to `/auth/register`, it will
# call the `register` view and use the return value as the response.
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()

    if form.validate_on_submit():
        print(form.data)
        error = None

        user = User.from_email(form)
        try:
            # how to handle error?
            db.session.add(user)
            db.session.commit()
        except db.IntegrityError:
            error = f"Email {user.email} is already registered."
        else:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        error = None
        user = db.session.execute(
            db.select(User).
            filter_by(email=form.email.data)
        ).scalar_one()

        if user is None:
            error = f"Email {form.email.data} is not registered"
        else:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/login.html", form=form)


# Now that the user's id is stored in the session, it will be available on
# subsequent requests. At the beginning of each request, it a user is
# logged in their information should be loaded and make available to
# other views.
# `bp.before_app_request()` registers a function that runs before the
# view function, no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_or_404(User, user_id)


# To log out, you need to remove the user id from the session.
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# A decorator to check if user logged.
# This decorator returns a new view function that wraps the original
# view it's applied to.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# Endpoints and URLs
# The url_for() function generates the URL to a view based on a name
# and arguments. The name associated with a view is also called the
# endpoint, and by default it's the same sa the name of the view function.
# When using a blueprint, the name of the blueprint is prepended to the name of the function.
