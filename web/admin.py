from app import app, User
from flask_login import current_user
from app import user_datastore


@app.route('/admin/list_users')
def list_users_view():
    admin_role = user_datastore.find_role('admin')
    if current_user.is_anonymous or admin_role not in current_user.roles:
        return 'admins only', 401
    return [
        dict(user=u.email, created_at=u.create_datetime)
        for u in User.query.all()
    ]
