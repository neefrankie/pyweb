from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/", methods=["GET"])
def register():
    return render_template("account/account.html")