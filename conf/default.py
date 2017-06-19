# coding:utf-8
debug = False  # TODO 这里要注意更改状态 每次上线保证状态为Flase
if debug:
    from settings_test import Config
else:
    from settings import Config

for conf_name in dir(Config()):  # 检测配置是是否被实现的同时 解压到全局变量中
    globals()[conf_name] = getattr(Config, conf_name)
