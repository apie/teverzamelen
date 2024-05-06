from functools import wraps
from flask import request, render_template
from flask_login import current_user
from app import app, db, APIKey, Item


@app.route('/api', methods=['GET', 'POST', 'DELETE'])
def api_page():
    api_key = None
    if not current_user.is_anonymous:
        if request.method == 'POST':
            all_existing = APIKey.query.filter_by(user=current_user).all()
            new_key = APIKey(user=current_user)
            for existing in all_existing:
                db.session.delete(existing)
            db.session.add(new_key)
            db.session.commit()
        if request.method == 'DELETE':
            APIKey.query.filter_by(user=current_user).delete()
            db.session.commit()
        api_key = APIKey.query.filter_by(user=current_user).first()
    return render_template('api.html', title='API overzicht', api_key=getattr(api_key, 'key', None))


def api_key_required(func):
    @wraps(func)
    def check_api_key(*args, **kwargs):
        if key := APIKey.query.filter_by(key=request.args.get('key')).first():
            return func(*args, **kwargs, key=key)
        return 'Geen toegang. Geldige API key nodig.', 401
    return check_api_key


@app.route('/api/reading_list')
@api_key_required
def api_reading_list(key):
    user = key.user
    return dict(
        user=user.email.split('@')[0],
        num_to_read=Item.query.filter_by(owned=True, read=False).join(Item.collection).filter_by(user=user).count(),
        num_busy_reading=Item.query.join(Item.collection).filter_by(user=user).join(Item.currently_reading).count(),
    )
