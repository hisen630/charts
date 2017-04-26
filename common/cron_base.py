# -*- coding: utf-8 -*-

import sys
import time
from crontab import CronTab

#add task
def _add_task(data):
    result = _add_task_db(data)
    #验证结果
    return result

#modify task
def _modify_task():
    result = _modify_task(data)
    #验证结果
    return result

#delete task
def _del_task():
    result = _del_task(data)
    return result

#add new job to crontab
def _add_new_job(comment,cmd,cycle):
    comment = str(comment)
    _cron = CronTab(user=True)
    jobs = _cron.find_comment(comment)
    c = 0
    for job in jobs:
        c += 1
    if c:
        pass
    else:
        job = _cron.new(command=cmd, comment=comment)
        job.setall(cycle)
        _cron.write()

#delete job from crontab
def _del_job(comment):
    _cron = CronTab(user=True)
    jobs = _cron.remove_all(comment=str(comment))
    _cron.write()

#modify job
def _modify_job(comment,cmd,cycle):
    _del_job(comment=str(comment))
    _add_new_job(comment,cmd,cycle)

#view crontab job
def _view_job(comment):
    _cron = CronTab(user=True)
    jobs = _cron.find_comment(str(comment))
    for job in jobs:
        print "find job:",job
