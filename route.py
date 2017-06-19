# -*- coding: utf-8 -*-
import os
import importlib
import inspect
from stat import S_ISDIR,S_ISREG
from flask import request
from flask.views import MethodView
from flask import Flask, url_for, session, request, jsonify, redirect
from hillinsight.storage import dbs
import os
from functools import wraps
from conf.default import IF_AUTH, AUTH_WHITE_LIST

if IF_AUTH:
    from hillinsight.web.auth import AuthManager, current_user, login_required, logout_user

class CustomView(MethodView):

    def dispatch_request(self, *args, **kwargs):
        path = request.path.split("/")
        if len(path) == 3:
            meth = getattr(self, path[-1], None)
            # meth = login_required(meth)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method
        return meth(*args, **kwargs)


class Route():
    def __init__(self,flask_app,DIR):
        self.__app = flask_app
        if IF_AUTH:
            ### define auth info
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
            domain = "sso.in.hillinsight.com"
            # domain = "sso.hillinsight.com:59687"
            self.__app.secret_key = os.environ.get('CLIENT_SECRET','WDRT6r081UBZqy7jiHRugbMheMbaDpls6cPH27jITbJH8K8DETmnWwDBsrSZ32WV')
            self.auth_manager = AuthManager(self.__app,
               consumer_key = os.environ.get('CLIENT_KEY', 'gg3IK199lZ1KVf8MPlzL0dSSpF2OZ2Y7'),
               consumer_secret = os.environ.get('CLIENT_SECRET','WDRT6r081UBZqy7jiHRugbMheMbaDpls6cPH27jITbJH8K8DETmnWwDBsrSZ32WV'),
               request_token_params={'scope': 'email'},
               base_url='http://sso.in.hillinsight.com/api/',
               request_token_url=None,
               access_token_url='http://{}/oauth/token'.format(domain),
               authorize_url='http://{}/oauth/authorize'.format(domain)
            )
            @self.__app.route('/logout')
            def logout():
                session.clear()
                logout_user()
                return redirect('http://{}/login'.format(domain));
            ###
        else:
            @self.__app.route('/logout')
            def logout():
                return redirect('/');
        self.__Dir = DIR
        self.viewControlDir = "{}/".format(DIR)
    def build(self):
        self.__make(self.viewControlDir)
    def __make(self,top):
        for f in os.listdir(top):
            if r".pyc" in f or f == r"__init__.py" or r".swp" in f:
                continue
            pathname = os.path.join(top, f)
            try:
                mode = os.stat(pathname).st_mode
            except PermissionError:
                continue
            else: 
                if S_ISDIR(mode): 
                    try:
                        self.__make(pathname) 
                    except PermissionError:
                        continue
                elif S_ISREG(mode):
                    self.url(pathname,f.replace(".py",""))
                else:
                    pass

    def user_required(self,f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if IF_AUTH:
                
                ### define auth info；you can define your self auth
                is_white = False
                try:
                    for item in AUTH_WHITE_LIST:
                        item = item.lower()
                        path = request.path.lower()
                        if path.startswith(item) and item != "/":
                            is_white = True
                except Exception, e:
                    pass
                if not is_white  and not (current_user.is_authenticated and session):
                    return self.__app.login_manager.unauthorized()
                ###

            return f(*args, **kwargs)
        return decorator

    def url(self,pathname,name):
        moduleStr = pathname.replace(".py","").replace("/",".")
        moduleObj = importlib.import_module(moduleStr)
        for classStr in dir(moduleObj):
            if not classStr.startswith("__") and classStr.lower()==name.lower():
                classObj = getattr(moduleObj, classStr)
                # load= getattr(obj, "Load")
                # inspect.getargspec(load) #获得方法参数
                obj = classObj()
                urlPath_low = pathname.replace(".py","").lower()
                urlPath_normal = pathname.replace(".py","")
                for methodName in dir(classObj):
                    if not methodName.startswith("__"):
                        urlPath = urlPath_low.replace(self.__Dir,"")
                        # view = getattr(obj, methodName)
                        # view = login_required(view)
                        view = self.user_required(obj.as_view(urlPath+"/"+methodName))
                        self.__app.add_url_rule(urlPath+"/"+methodName.lower(), endpoint=urlPath+"/"+methodName, view_func=view,methods=["GET","POST"])
                        urlPath = urlPath_normal.replace(self.__Dir,"")
                        self.__app.add_url_rule(urlPath+"/"+methodName.lower(), endpoint=urlPath+"/"+methodName, view_func=view,methods=["GET","POST"])