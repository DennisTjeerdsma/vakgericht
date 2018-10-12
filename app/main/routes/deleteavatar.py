from app.main import bp
from flask_login import login_required
from flask import redirect, current_app, url_for
from app.models import User
from app import db
import os

@bp.route("/delete_avatar/<user_id>")
@login_required
def delete_avatar(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if user.avatar != "vakgericht.jpeg":
        os.remove(os.path.join(current_app.config["UPLOADED_AVATARS_DEST"], user.avatar))
        user.avatar = "vakgericht.jpeg"
    db.session.commit()
    return redirect(url_for("main.edit_profile"))