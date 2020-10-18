from flask_restless import ProcessingException
from flask import redirect, url_for, request
from flask_login import current_user
from flask_security import Security, auth_required

from app import app, user_datastore, Collection
security = Security(app, user_datastore)

@security.unauthn_handler
def r(*args, headers):
        if 'api/' in request.url:
            #Needed for auth_func because it needs to raise something. Return values dont matter.
            raise ProcessingException(description='Not Authorized', code=401)
        #Otherwise, normal behavior: redirect to login page
        return redirect(url_for('security.login'))


@auth_required()
def auth_func_single(instance_id=None, **kwargs):
        if ('data' in kwargs and kwargs['data']['user_id'] != current_user.id) or (Collection.query.filter_by(user=current_user, id=instance_id).first() is None):
            # Changed the user OR instance_id was not found for the current user
            raise ProcessingException(description='Not Authorized', code=401)

@auth_required()
def auth_func_many(search_params=None, **kwargs):
        if 'filters' not in search_params:
            search_params['filters'] = []
        # Always filter on current logged in user
        search_params['filters'].append(
            dict(name='user', op='eq', val=current_user)
        )

def deny(*args, **kwargs):
        raise ProcessingException(description='Forbidden', code=403)

def auth_func_post(data, **kwargs):
        if data['user_id'] != current_user.id:
            # Can only post for the current user
            raise ProcessingException(description='Not Authorized', code=401)


@auth_required()
def auth_func_single_item(instance_id=None, **kwargs):
        if Collection.query.filter_by(user=current_user, id=kwargs['data']['collection_id']).first() is None:
            # collection_id was not found for the current user
            raise ProcessingException(description='Not Authorized', code=401)

@auth_required()
def auth_func_many_item(search_params=None, **kwargs):
        if 'filters' not in search_params:
            search_params['filters'] = []
        # Always filter on current logged in user
        search_params['filters'].append(
            dict(name='collection__user', op='eq', val=current_user)
        )

def auth_func_post_item(data, **kwargs):
        if Collection.query.filter_by(user=current_user, id=data['collection_id']).first() is None:
            # Can only post for collections owned by the current user
            raise ProcessingException(description='Not Authorized', code=401)

general_preprocessor=dict(
    PUT_MANY=[deny],
    DELETE_MANY=[deny],
)
check_user=dict(
    GET_SINGLE=[auth_func_single],
    GET_MANY=[auth_func_many],
    POST=[auth_func_post],
    PUT_SINGLE=[auth_func_single],
    DELETE_SINGLE=[auth_func_single],
)
check_user_item=dict(
    GET_SINGLE=[auth_func_single_item],
    GET_MANY=[auth_func_many_item],
    POST=[auth_func_post_item],
    PUT_SINGLE=[auth_func_single_item],
    DELETE_SINGLE=[auth_func_single_item],
)

