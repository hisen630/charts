#!/usr/bin/env python2.7
#coding=utf-8

from hillinsight.brand import utils
import sys
import argparse
import json

from hillinsight.storage import dbs

BRAND_TABLE='t_hh_brands_repo_copy'

db = dbs.create_engine('hillinsight', master=True)

g_project = "__all__"
g_alias_norm_mapping = {} # alias -> Brand set
g_pattern_norm_mapping = {} # pattern -> Brand set

class Brand(object):

    def __init__(self):
        self.id = None
        self.project = None
        self.priority = None
        self.display_name = None
        self.normalized_name = None
        self.precise_alias_dict = {} # alias -> {}, property -> value, 精确的一一对应别名
        self.pattern_alias_dict = {} # alias_pattern -> {}, property -> value, 正则表达式的列表
        self.merged2id = None # 若该字段非None，则它应当被归一到值所对应的品牌
        self.from_key = None
        self.description = None

    def add_alias(self, _unicode):
        if _unicode not in self.precise_alias_dict:
            self.precise_alias_dict[_unicode] = {}

    
    def merge(self, another):
        if another.priority > self.priority:
            self.priority = another.priority

        if another.description and not self.description:
            self.description = another.description

        for alias in another.precise_alias_dict.keys():
            if alias not in self.precise_alias_dict:
                #print >> sys.stderr, '[DEBUG] Merging [{}]'.format(alias.encode('utf-8'))
                self.precise_alias_dict[alias] = {'type':'merged', 'id':another.id}

        for p in another.pattern_alias_dict.keys():
            if p not in self.pattern_alias_dict:
                self.pattern_alias_dict[p] = {'type':'merged', 'id':another.id}

    def to_dict(self):
        out_dict = {}
        out_dict['id'] = self.id
        out_dict['project'] = self.project
        out_dict['display_name'] = self.display_name
        out_dict['priority'] = self.priority
        out_dict['normalized_name'] = self.normalized_name
        out_dict['precise_alias_dict'] = self.precise_alias_dict
        out_dict['pattern_alias_dict'] = self.pattern_alias_dict
        out_dict['merged2id'] = self.merged2id
        out_dict['from_key'] = self.from_key

        return out_dict


    @staticmethod
    def from_str(_unicode, project):
        inst = Brand()
        inst.project = project
        inst.display_name = _unicode.strip() # do not use normalize, just strip is enough
        inst.normalized_name = utils.normalize_brand(_unicode)
        if len(inst.normalized_name) == 0:
            return None
        inst.add_alias(inst.normalized_name)
        return inst

    @staticmethod
    def from_dict(dic):
        inst = Brand()
        inst.id = dic['id']
        inst.project = dic['project']
        inst.priority = dic['priority']
        inst.display_name = dic['display_name']
        inst.normalized_name = dic['normalized_name']
        if dic['precise_alias_dict']:
            inst.precise_alias_dict = json.loads(dic['precise_alias_dict'])
        else:
            inst.precise_alias_dict = {}
        if dic['pattern_alias_dict']:
            inst.pattern_alias_dict = json.loads(dic['pattern_alias_dict'])
        else:
            inst.pattern_alias_dict = {}
        inst.merged2id = dic['merged2id']
        inst.description = dic['description']
        inst.from_key = dic['from_key']
        return inst


def _read_brands_file(filename, priority_min):
    brands_dict = {} # brands_name -> priority
    with open(filename, 'rb') as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            l = l.decode('utf-8')
            eles = l.split('\t')
            if len(eles) != 2:
                print >> sys.stderr, '[WARNING]Line [{}] should be two columns.'.format(l)
                continue
            if not eles[0].strip():
                continue
            brand_name, priority = eles[0], float(eles[1])
            if priority < priority_min:
                continue
            brands_dict[brand_name] = priority
    print >> sys.stderr, '[INFO]Read in {} brands.'.format(len(brands_dict))
    return brands_dict


def _load_brands_norm():

    brands_dict = {} # id -> Brand

    res = db.select(BRAND_TABLE, where={'project':g_project})
    for rec in res:
        brands_dict[rec['id']] = Brand.from_dict(rec)

    for rec_id, brand in brands_dict.items():
        # it could be a merge chain, follow up
        while brand.merged2id:
            assert brand.merged2id in brands_dict, "ID[{}] is merged to ID[{}], but ID[{}] cannot be found.".format(rec_id, brand.merged2id, brand.merged2id)
            brands_dict[brand.merged2id].merge(brand)
            brand = brands_dict[brand.merged2id]

    return set(filter(lambda x:x.merged2id is None, brands_dict.values()))
    
def make_norm_mapping():

    brands_set = _load_brands_norm()

    global g_alias_norm_mapping
    global g_pattern_norm_mapping

    for brand in brands_set:
        for alias in brand.precise_alias_dict.keys():
            if alias not in g_alias_norm_mapping:
                g_alias_norm_mapping[alias] = set((brand,))
            else:
                g_alias_norm_mapping[alias].add(brand)

        for pattern in brand.pattern_alias_dict.keys():
            p = re.compile(pattern)
            if p not in g_pattern_norm_mapping:
                g_pattern_norm_mapping[p] = set((brand,))
            else:
                g_pattern_norm_mapping[p].add(brand)

    ambiguous_set = filter(lambda x:len(x[1])>1, g_alias_norm_mapping.items())
    for alias, brand_list in ambiguous_set:
        am_str = ', '.join(['['+b.display_name+']' for b in brand_list])
        print >> sys.stderr, '[WARNING] Alias[{}] is ambiguous for {}'.format(alias.encode('utf-8'), am_str.encode('utf-8'))

    ambiguous_set = filter(lambda x:len(x[1])>1, g_pattern_norm_mapping.items())
    for p, brand_set in ambiguous_set:
        am_str = ', '.join(['['+b.display_name+']' for b in brand_set])
        print >> sys.stderr, '[WARNING] Pattern[{}] is ambiguous for {}'.format(p.pattern.encode('utf-8'), am_str.encode('utf-8'))


def match(brand_unicode, project=g_project):

    global g_project
    assert isinstance(brand_unicode, (unicode, str)), 'Brand must be either a string or a unicode, but received [{}]'.format(type(brand_unicode))

    if isinstance(brand_unicode, str):
        brand_unicode = brand_unicode.decode('utf-8')

    if not g_alias_norm_mapping or project != g_project:
        g_project = project
        make_norm_mapping()
    
    norm_brand = utils.normalize_brand(brand_unicode)
    brand_set = g_alias_norm_mapping.get(norm_brand, None)
    if brand_set:
        brand_list = list(brand_set)
        brand_list.sort(key=lambda x:x.priority, reverse=True)
        #return [(b.display_name, b.project, b.from_key) for b in brand_list], 'alias'
        return brand_list, 'alias'

    for p, brand_set in g_pattern_norm_mapping.items():
        if p.search(norm_brand):
            brand_list = list(brand_set)
            brand_list.sort(key=lambda x:x.priority, reverse=True)
            #return [(b.display_name, b.project, b.from_key) for b in brand_list], 'pattern'
            return brand_list, 'pattern'

    return [], 'Not found'


def _add_one_brand(brand_unicode, project, split, priority, from_key):

    global g_alias_norm_mapping
    brand_list, how_str = match(brand_unicode)

    if not brand_list:
        brand_obj = Brand.from_str(brand_unicode, project)
        if not brand_obj:
            return None
        brand_obj.priority = priority
        brand_obj.from_key = from_key

        norm_brand = utils.normalize_brand(brand_unicode)
        assert norm_brand not in g_alias_norm_mapping, "Brand[{}] should not in g_alias_norm_mapping".format(brand_unicode.encode('utf-8'))
        g_alias_norm_mapping[norm_brand] = set((brand_obj,))

        brand_eles = filter(lambda x:len(x)>1, [utils.normalize_brand(e) for e in norm_brand.split(split)])
        if len(brand_eles) == 2:
            # esas/伊萨斯 -> 伊萨斯/esas
            brand_eles.append(brand_eles[1] + split + brand_eles[0])
            # esas/伊萨斯 -> esas伊萨斯
            brand_eles.append(brand_eles[0] + brand_eles[1])
            # esas/伊萨斯 -> 伊萨斯esas
            brand_eles.append(brand_eles[1] + brand_eles[0])

        for e in brand_eles:
            brand_obj.add_alias(e) # add alias to it's own
            if e not in g_alias_norm_mapping:
                g_alias_norm_mapping[e] = set((brand_obj,))
            else:
                g_alias_norm_mapping[e].add(brand_obj)

        return brand_obj

    return None



def _add_brands(brands_dict, project, split, from_key):

    brands_list = brands_dict.items()
    brands_list.sort(key=lambda x:x[1], reverse=True)

    new_brand_set = set()

    # 优先正规名称(如 "Maybelline/美宝莲")
    for brand_unicode, priority in brands_list:
        if brand_unicode.find(split) > 0:
            brand_obj = _add_one_brand(brand_unicode, project, split, priority, from_key)
            if brand_obj:
                new_brand_set.add(brand_obj)

    # 非正规名
    for brand_unicode, priority in brands_list:
        if brand_unicode.find(split) == -1:
            brand_obj = _add_one_brand(brand_unicode, project, split, priority, from_key)
            if brand_obj:
                new_brand_set.add(brand_obj)
    
    return new_brand_set
    

def output(brand_set, test=True):
    print >> sys.stderr, '[INFO] Outputing new built brands.'
    if test:
        for b in brand_set:
            print >> sys.stderr, '[TEST DUMP]', json.dumps(b.to_dict())
        return
    else:
        for b in brand_set:
            #print >> sys.stderr, '[DEBUG]', b.display_name.encode('utf-8')
            out_dict = b.to_dict()
            for k in out_dict.keys():
                if not out_dict[k]:
                    out_dict.pop(k)
                elif isinstance(out_dict[k], dict):
                    out_dict[k] = json.dumps(out_dict[k])
            db.insert(BRAND_TABLE, **out_dict)

    for alias, brand_set in g_alias_norm_mapping.items():
        if len(brand_set) != 1:
            am_str = ', '.join(['['+b.display_name+']' for b in brand_set])
            print >> sys.stderr, '[WARINING][OUTPUT] Alias [{}] is ambiguous for {}'.format(alias.encode('utf-8'), am_str.encode('utf-8'))


def batch_add(filename, project, split, test, priority, from_key):

    make_norm_mapping()

    # brand_str -> priority
    brands_dict = _read_brands_file(filename, priority)
    new_brands_set = _add_brands(brands_dict, project, split, from_key)
    print >> sys.stderr, '[INFO] {} new brands built.'.format(len(new_brands_set))
    output(new_brands_set, test)

def run(project=g_project,filename,split="/",test,Priority=10000,from_key):
    import os
    if not os.path.exists(filename):
        print >> sys.stderr, '[ERROR]\tFile "{}" does not exist.'.format(filename)
        sys.exit(1)

    batch_add(filename, project, split=split, test=test, priority=Priority, from_key=from_key)
    print >> sys.stderr, '[INFO] Job done.'

# if '__main__' == __name__:

#     parser = argparse.ArgumentParser(description="将品牌列表刷入品牌库")
#     parser.add_argument('-p', '--project', type=str, default=g_project, help='默认是\'__all__\'')
#     parser.add_argument('-f', '--filename', type=str, help='品牌列表文件，应为utf-8格式编码。内容应当是两列(tab分隔)，第一列是品牌名称，第二列是其对应的权重', required=True)
#     parser.add_argument('-s', '--split', type=str, default='/', help='品牌内部的分隔符，默认是/')
#     parser.add_argument('-t', '--test', action='store_true', help='测试模式，不会写库')
#     parser.add_argument('-P', '--Priority', type=float, default=10000, help='优先级最小值。很多时候优先级实际上是品牌对应的某月销售额。销售额低的出现脏数据的概率大。默认值10,000')
#     parser.add_argument('-F', '--from_key', type=str, help='用以标识数据来源，如\'taobao_29\'来自淘宝的类目id为29的类目。', required=True)

#     args = parser.parse_args()

#     import os
#     if not os.path.exists(args.filename):
#         print >> sys.stderr, '[ERROR]\tFile "{}" does not exist.'.format(args.filename)
#         sys.exit(1)

#     batch_add(args.filename, args.project, split=args.split, test=args.test, priority=args.Priority, from_key=args.from_key)
#     print >> sys.stderr, '[INFO] Job done.'
