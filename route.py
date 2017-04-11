# -*- coding: utf-8 -*-
import os
import importlib
import inspect
from stat import S_ISDIR,S_ISREG
class Route():
    def __init__(self,flask_app,DIR):
        self.__app = flask_app
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
                        self.__app.add_url_rule(urlPath+"/"+methodName.lower(), endpoint=urlPath+"/"+methodName, view_func=getattr(obj, methodName),methods=["GET","POST"])
                        urlPath = urlPath_normal.replace(self.__Dir,"")
                        self.__app.add_url_rule(urlPath+"/"+methodName.lower(), endpoint=urlPath+"/"+methodName, view_func=getattr(obj, methodName),methods=["GET","POST"])
