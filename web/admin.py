from app import app, User
from flask_security import roles_required


@app.route('/admin/list_users')
@roles_required('admin')
def list_users_view():
    return [
        dict(user=u.email, created_at=u.create_datetime)
        for u in User.query.all()
    ]
