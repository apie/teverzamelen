from app import app, User
from flask_security import roles_required
from flask import request


@app.route("/admin/list_users")
@roles_required("admin")
def list_users_view():
    active = request.args.get("active", "")
    confirmed = request.args.get("confirmed", "")
    user_list = User.query.all()
    if active != "":
        active = active == "true"
        user_list = filter(lambda u: u.active == active, user_list)
    if confirmed != "":
        confirmed = confirmed == "true"
        user_list = filter(
            lambda u: (u.confirmed_at is not None) is confirmed,
            user_list,
        )
    return [
        dict(
            user=u.email,
            created_at=u.create_datetime,
            confirmed_at=u.confirmed_at,
            active=u.active,
        )
        for u in user_list
    ]
