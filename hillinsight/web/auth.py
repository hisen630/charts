from flask import Flask, url_for, session, request, jsonify, redirect
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask_oauthlib.client import OAuth
from hillinsight.storage import dbs
from hillinsight.storage.db_conn import _mysql_config
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

class User(object):
    def __init__(self, user_name):
        self.db = _mysql_config['sso']['master']['online']
        rows = self.db.query("select * from t_sso_user where name = $name", vars = {"name": user_name})
        if len(rows) == 1:
            self.is_active = True
            self.is_authenticated = True
            self.is_anonymous = False
            data = rows[0]
            self.id = data["id"]
            self.name = data["name"]
            self.name_english = data["name_english"]
            self.email = data["email"]
            #if data['avatar_path'] != None:
            self.avatar = data["avatar_path"]
            #else:
            #    self.avatar = data["avatar_path"]
            self.userInfo = data
        else:
            self.is_active = False
            self.is_authenticated = False
            self.is_anonymous = False
            self.name = False
            self.userInfo = {}


    def __getattr__(self, name):
        value = False
        if name in self.userInfo:
            value = self.userInfo[name]
        return value

    def get_id(self):
        return self.name

class AuthManager(object):

    def __init__(self, app, **kwargs):
        login_manager = LoginManager()
        login_manager.session_protection = "strong"
        login_manager.login_view = "login"
        login_manager.init_app(app)
        self.obj = login_manager
        oauth = OAuth(app)
        remote = oauth.remote_app('remote', **kwargs)
        @login_manager.unauthorized_handler
        def unauthorized():
            next_url = request.args.get('next') or request.referrer or request.url or None
            #next_url = None
            return remote.authorize(
                callback=url_for('authorized', next=next_url, _external=True)
            )

        @app.route('/authorized')
        def authorized():
            resp = remote.authorized_response()
            if resp is None:
                return 'Access denied: reason=%s error=%s' % (
                    request.args['error_reason'],
                    request.args['error_description']
                )
            session['remote_oauth'] = (resp['access_token'], '')
            resp = remote.get('me')
            next =  request.args['next']
            login_user(User(resp.data["name"]))
            return redirect(next)

        @remote.tokengetter
        def get_oauth_token():
            return session.get('remote_oauth')

        @login_manager.user_loader
        def load_user(user_id):
            return User(user_id)


# if __name__ == '__main__':
#     us = User('panwei')
#     print us.userInfo
