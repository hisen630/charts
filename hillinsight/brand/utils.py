#!/usr/bin/env python2.7
#coding=utf-8

import re
import HTMLParser
import urllib2

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring


def normalize_brand(_unicode, html_escape=True, url_unquote=True, strip=True, lower=True, q2b=True, del_brackets=True, split_symbol='/', delete_symbols='''.'`·'''):
    """对品牌名称进行归一化.

    :param _unicode: 
    :param html_escape: 
    :param url_unquote: 
    :param strip: 
    :param lower: 
    :param q2b: 
    :param del_brackets: 
    :param split_symbol: 
    :param delete_symbols: 
    :return: s

    """
    assert isinstance(_unicode, unicode)

    original_unicode = _unicode

    if html_escape: # html标记转义
        htmlparser = HTMLParser.HTMLParser()
        _unicode = htmlparser.unescape(_unicode)

    if url_unquote: # url转义
        _unicode = urllib2.unquote(_unicode)
    if q2b:
        _unicode = strQ2B(_unicode)
    if lower:
        _unicode = _unicode.lower()

    # chinese punc trans to en punc
    for cp, ep in {
        u'“':u'"',
        u'”':u'"',
        u'·':u'.',
        u'。':u'.',
        u'！':u'!',
        u'……':u'......',
        u'（':u'(',
        u'）':u')',
        u'——':u'--',
        u'【':u'[',
        u'】':u']',
        u'{':u'{',
        u'}':u'}',
        u'‘':u'\'',
        u'’':u'\'',
        u'，':u',',
        u'？':u'?',
        u'：':u':',
        u'；':u';',
        u'《':u'<',
        u'》':u'>'}.items():
        _unicode = re.sub(cp, ep, _unicode)
    
    # latin to ascii, u'Amopé' -> u'Amope'
    for lt, en in {
        u'ı':u'i', u'ì':u'i', u'í':u'i', u'î':u'i', u'ï':u'i',
        u'İ':u'I', u'Ì':u'I', u'Í':u'I', u'Î':u'I', u'Ï':u'I',
        u'ö':u'o', u'ó':u'o', u'ò':u'o', u'ô':u'o', u'õ':u'o', u'ø':u'o',
        u'Ö':u'O', u'Ò':u'O', u'Ó':u'O', u'Ô':u'O', u'Õ':u'O', u'Ø':u'O',
        u'ü':u'u', u'ù':u'u', u'ú':u'u', u'û':u'u',
        u'Ü':u'U', u'Ù':u'U', u'Ú':u'U', u'Û':u'U',
        u'à':u'a', u'á':u'a', u'â':u'a', u'ã':u'a', u'ä':u'a', u'å':u'a',
        u'À':u'A', u'Á':u'A', u'Â':u'A', u'Ã':u'A', u'Ä':u'A', u'Å':u'a',
        u'æ':u'ae', u'Æ':u'AE',
        u'è':u'e', u'é':u'e', u'ê':u'e', u'ë':u'e',
        u'È':u'E', u'É':u'E', u'Ê':u'E', u'Ë':u'E',
        u'ñ':u'n', u'Ñ':u'N',
        u'ý':u'y', u'ÿ':u'y', u'Ý':u'Y', u'Ÿ':u'Y',
        u'ş':u's', u'Ş':u'S',
        u'ç':u'c', u'Ç':u'C',
        u'ğ':u'g', u'Ğ':u'G'
        }.items():
        _unicode = re.sub(lt, en, _unicode)
    
    _unicode = re.sub(r'\s+', ' ', _unicode) # 连续多空白符转为单个空格
    _unicode = re.sub(r'{}+'.format(split_symbol), split_symbol, _unicode) # 连续多个切分符转换为单个切分符，如"SHINO//丝诺"

    if strip:
        _unicode = _unicode.strip()
    if del_brackets:
        _unicode = re.sub(r'(\(.*?\))', '', _unicode) # 删除括号中的内容

    _unicode = re.sub(r'\s*{}\s*'.format(split_symbol), split_symbol, _unicode) # 删除品牌内部分隔符前后空格
    if delete_symbols:
        _unicode = re.sub(r'[{}]'.format(delete_symbols), '', _unicode) # 删除一些无用的标点符号

    return _unicode

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False
 
def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False
 
def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False
 
def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False
def _get_dedup_empty():
    """将连续空白符替换成单个空白符"""
    import re
    multi_empty_p = re.compile(r'\s{2,}')
    
    def _dedup_empty(ustr):
        return multi_empty_p.subn(u' ', ustr)[0]
    return _dedup_empty

dedup_empty = _get_dedup_empty()

def _get_remove_bracket():
    """去掉括号内的信息"""
    import re
    bracket_p = re.compile(r'(\(.*\))')
    
    def _remove_bracket(ustr):
        return bracket_p.subn(u'', ustr)[0]
    return _remove_bracket

remove_bracket = _get_remove_bracket()


def split_by_cn_en(ustring):
    """将ustring按照中文，字母分开"""
    retList=[]
    utmp=[]
    _state = 0 # 0非中文，1非英文
    _split = False # 当前状态是否产生一个分割
    for uchar in ustring:
        if is_chinese(uchar):
            if _state == 0:
                _split = True
            _state = 1
                
        elif is_alphabet(uchar):
            if _state == 1:
                _split = True
            _state = 0

        if _split:
            if len(utmp) > 0:
                retList.append(''.join(utmp))
                utmp = []
            _split = False
            
        utmp.append(uchar)
    
    if len(utmp) > 0:
        retList.append(''.join(utmp))
        
    return retList

def array_column(data,format,format_str=False):
    """取list或者dict 二级下面的某列，比如 直接从数据库返回的结果我想取name列，[{'name'：'fds','id':1},{'name':'fdsa','id':2}]"""
    result = []
    if type(format) == str:
        if format.strip() == '':
            pass
        else:
            if type(data) == list:
                for i in data:
                    if format_str and ( type(i[format]) == datetime.date or type(i[format]) == datetime.datetime):
                        result.append(i[format].isoformat())
                    else:
                        result.append(i[format])
            elif type(data) == dict:
                for idx,i in enumerate(data):
                    if format_str and ( type(i[format]) == datetime.date or type(i[format]) == datetime.datetime):
                        result.append(i[format].isoformat())
                    else:
                        result.append(i[format])
    return result
def dbFormatToDict(data,format):
    """从list或者dict里面以某列数据作为dict 的index 比如从数据库返回的结果我将name列作为index变为dict，[{'name'：'fds','id':1},{'name':'fdsa','id':2}]"""
    result = {}
    if type(format) == str:
        if format.strip() == '':
            result = data
        else:
            for i in data:
                result[i[format]] = i
    elif (type(format) == list and format) or (type(format) == dict and format):
        for i in data:
            index = ''
            for j in format:
                index += i[j]
            result[index] = i
    return result