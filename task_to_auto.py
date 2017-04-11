# -*- coding: utf-8 -*-
from common.task_run_base import handle

if '__main__' == __name__:
    msg = handle()
    for item in msg:
        print item
