# -*- coding: utf-8 -*-
from base import base_b
from common.utils import dbFormatToDict
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_menus(url):
    menus = base_b.get_menus()
    menus_dict = dbFormatToDict(menus,"id")
    current_id = 0
    level = 0
    menus_result_dict = {}
    for key in menus_dict:
        item = menus_dict[key]
        if item['parent_id'] in menus_result_dict:
            menus_result_dict[item['parent_id']].append(item)
        else:
            menus_result_dict[item['parent_id']] = [item]
        if item['url'] in url:
            if level < item['level']:
                current_id = item['id']
    result = {}
    result['bread_crumbs'] = []
    if current_id:
        tmp = get_bread_crumbs(current_id,menus_dict,[])
        result['bread_crumbs'] = tmp[::-1]
        result['title'] = tmp[0]
    result['menus'] = get_relation(0,menus_result_dict,menus_dict)
    return result

def get_bread_crumbs(ids,menus_dict,result=[]):
    if ids in menus_dict:
        result.append(menus_dict[ids]['name'])
        result = get_bread_crumbs(menus_dict[ids]['parent_id'],menus_dict,result)
    return result

def get_relation(parent_id,menus_result_dict,menus_dict):
    result = []
    if parent_id in menus_result_dict:
        for item in menus_result_dict[parent_id]:
            tmp = item
            child = get_relation(item['id'],menus_result_dict,menus_dict)
            if child:
                tmp['child'] = child
            else:
                tmp['child'] = []
            result.append(tmp)
    if result:
        result.sort(menus_comp)
    return result

def menus_comp(x,y):
    if x['sort'] < y['sort']:
        return -1
    elif x['sort'] > y['sort']:
        return 1
    else:
        if x['id'] < y['id']:
            return -1
        elif x['id'] > y['id']:
            return 1
        else:
            return 0