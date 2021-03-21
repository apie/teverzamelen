#!/usr/bin/env python3
import os

import flask
import flask_sqlalchemy
from flask import redirect, url_for, request, send_from_directory, render_template, render_template_string, Response
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore
from flask_security.models import fsqla_v2 as fsqla
from flask_security import Security
from flask_login import current_user
from flask_security import auth_required

import config

app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_DEFAULT_REMEMBER_ME'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/'
app.config['SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL'] = False
app.config['SECURITY_EMAIL_SUBJECT_REGISTER'] = 'Account aangemaakt! Welkom bij Teverzamelen'

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
mail = Mail(app)
# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = config.SECRET_KEY
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = config.SECURITY_PASSWORD_SALT

# As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
# underlying engine. This option makes sure that DB connections from the
# pool are still valid. Important for entire application since
# many DBaaS options automatically close idle connections.
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}

db = flask_sqlalchemy.SQLAlchemy(app)

app.config['DEBUG'] = config.DEBUG


class Collection(db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref('collections', lazy='dynamic'))
    name = db.Column(db.String(255))
    public = db.Column(db.Boolean(), default=False)


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    collection = db.relationship("Collection", backref=db.backref('items', lazy='dynamic'))
    sequence = db.Column(db.Integer)
    name = db.Column(db.String(255))
    owned = db.Column(db.Boolean(), default=False)
    want = db.Column(db.Boolean(), default=False)
    read = db.Column(db.Boolean(), default=False)


# Define models
fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    pass


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
db.create_all()
security = Security(app, user_datastore)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    collections = to_read = ()
    if not current_user.is_anonymous:
        collections = Collection.query.filter_by(user=current_user)
        to_read = Item.query.filter_by(owned=True, read=False).join(Item.collection).filter_by(user=current_user).count()
    return render_template('index.html', title='Welkom', collections=collections, to_read=to_read)


@app.route('/public')
def public():
    users = User.query.join(User.collections).filter_by(public=True)
    return render_template('public/public_index.html', title='Gedeelde lijstjes', users=users)

@app.route('/public/user/<id_or_email>')
def public_user(id_or_email):
    user = User.query.filter_by(id=id_or_email).first() or User.query.filter_by(email=id_or_email).first()
    if not user:
        return 'Unknown user', 404
    collections = Collection.query.filter_by(public=True, user=user)
    return render_template('public/public_collection.html', title=f"Gedeelde lijstjes van {user.email.split('@')[0]}", collections=collections)

@app.route('/public/collection/<id>')
def view_public_collection(id):
    collection = Collection.query.filter_by(public=True, id=id).first_or_404()
    return render_template(
        'public/view_public_collection.html',
        title=f'Bekijk gedeeld lijstje "{collection.name}" van {collection.user.email.split("@")[0]}',
        collection=collection,
        in_my_collection=False if current_user.is_anonymous else Collection.query.filter_by(user=current_user, name=collection.name).count() > 0,
    )

def delete_collection(collection):
    # TODO direct teruggaan
    Item.query.filter_by(collection=collection).delete()
    Collection.query.filter_by(id=collection.id).delete()
    db.session.commit()
    return '<a href="/">back</a>'

def patch_collection(collection):
    field = request.environ['HTTP_HX_TRIGGER_NAME']
    val = getattr(collection, field)
    if isinstance(val, bool):
        newval = not val
        retval = 'Ja' if newval else 'Nee'
    else:
        raise Exception('Not implemented')
    Collection.query.filter_by(id=collection.id).update({field: newval})
    db.session.commit()
    if field == 'public':
        return render_template('partials/is_public.html', collection=collection)
    return retval

@app.route('/collection/<id>', methods=['GET', 'DELETE', 'PATCH'])
@auth_required()
def view_collection(id):
    collection = Collection.query.filter_by(user=current_user, id=id).first_or_404()
    if request.method == 'DELETE':
        return delete_collection(collection)
    elif request.method == 'PATCH':
        return patch_collection(collection)
    return render_template('view_collection.html', title=f'Bewerk lijstje "{collection.name}"' , collection=collection)


@app.route('/collection/new', methods=['POST'])
@auth_required()
def new_collection():
    name = request.form['name']
    new_collection = Collection(name=name, user=current_user)
    db.session.add(new_collection)
    db.session.commit()
    return redirect(f'/collection/{new_collection.id}')


@app.route('/copy_collection/<id>', methods=['POST'])
@auth_required()
def copy_collection(id):
    # Copy the collection and all the items in it.
    # Only copy names. Not owned/read attributes.
    collection = Collection.query.filter_by(public=True, id=id).first_or_404()
    new_collection = Collection(name=collection.name, user=current_user)
    db.session.add(new_collection)
    db.session.commit()
    for i, item in enumerate(collection.items.all()):
        item_i = Item(name=item.name, collection=new_collection)
    db.session.commit()
    return redirect(f'/collection/{new_collection.id}')


@app.route('/item/new', methods=['POST'])
@auth_required()
def new_item():
    collection_id = request.form['collection_id']
    name = request.form['name']
    collection = Collection.query.filter_by(user=current_user, id=collection_id).first()
    item = Item(name=name, collection=collection)
    db.session.add(item)
    db.session.commit()
    return render_template('partials/item_tr.html', item=item)


@app.route('/item/<id>', methods=['PATCH', 'DELETE'])
@auth_required()
def change_item(id):
    item = Item.query.filter_by(id=id).first()
    if item.collection.user != current_user:
        return 'Unauthorized', 401
    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return ''
    if request.method == 'PATCH':
        field = request.environ['HTTP_HX_TRIGGER_NAME']
        val = getattr(item, field)
        if isinstance(val, bool):
            newval = not val
        else:
            raise Exception('Not implemented')
        Item.query.filter_by(id=id).update({field: newval})
        db.session.commit()
        if request.environ['HTTP_REFERER'].endswith('reading_list'):
            return '' # Item marked as read. Do not return anything
        return render_template('partials/item_tr.html', item=item)


@app.route('/reading_list')
@auth_required()
def reading_list():
    collections = Collection.query.filter_by(user=current_user)
    to_read = Item.query.filter_by(owned=True, read=False).join(Item.collection).filter_by(user=current_user)
    return render_template('reading_list.html', title='Leeslijst', to_read=to_read)


if __name__ == '__main__':
    app.run()
