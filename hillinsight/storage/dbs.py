#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from web import SQLQuery,SQLParam
from random import choice
from .common import _mysql_config
import os
import sys
import platform
import types
web.config.debug = False
sqlparam =  SQLParam

def create_engine(name, master=False, online=False,pooling = True):
    # configs = load_mysql_config()
    configs = _mysql_config
    key = name + ("_online" if online else "_offline")
    config = configs.get(key, None)
    if config == None:
        return None
    config = config.get("master" if master else "slave", None)
    if config == None:
        return None
    if master == False and len(config) > 0:
        config = choice(config)
    if config == None:
        return None
    db = web.database(dbn="mysql", db=config["db"], host=config["host"], port=int(config["port"]), user=config["user"], pw=config["pw"], pooling=pooling)
    db.replace = types.MethodType(replace, db)
    db.multiple_replace = types.MethodType(multiple_replace, db)
    db.insert_ignore = types.MethodType(insert_ignore, db)
    db.multiple_insert_ignore = types.MethodType(multiple_insert_ignore, db)
    db.columns_name = types.MethodType(columns_name, db)
    return db

def create_engine_custom(dbn="mysql",db="",host="",port="",user="",pw=""):
    db = web.database(dbn=dbn,db=db,host=host,port=port,user=user,pw=pw)
    db.replace = types.MethodType(replace, db)
    db.multiple_replace = types.MethodType(multiple_replace, db)
    db.insert_ignore = types.MethodType(insert_ignore, db)
    db.multiple_insert_ignore = types.MethodType(multiple_insert_ignore, db)
    db.columns_name = types.MethodType(columns_name, db)
    return db

def columns_name(self, sql_query):
        names = []
        
        db_cursor = self._db_cursor()
        db_cursor.execute(sql_query)
        
        if db_cursor.description:
            names = [x[0] for x in db_cursor.description]
        return names

def replace(self, tablename, seqname=None, _test=False, **values): 
    """
    Inserts `values` into `tablename`. Returns current sequence ID.
    Set `seqname` to the ID if it's not the default, or to `False`
    if there isn't one.
        >>> db = DB(None, {})
        >>> q = db.insert('foo', name='bob', age=2, created=SQLLiteral('NOW()'), _test=True)
        >>> q
        <sql: "REPLACE INTO foo (age, name, created) VALUES (2, 'bob', NOW())">
        >>> q.query()
        'REPLACE INTO foo (age, name, created) VALUES (%s, %s, NOW())'
        >>> q.values()
        [2, 'bob']
    """
    def q(x): return "(" + x + ")"
    if values:
        _keys = SQLQuery.join(values.keys(), '`,`',prefix='`', suffix='`')
        _values = SQLQuery.join([sqlparam(v) for v in values.values()], ', ')
        sql_query = "REPLACE INTO %s " % tablename + q(_keys) + ' VALUES ' + q(_values)
    else:
        sql_query = SQLQuery("REPLACE INTO %s DEFAULT VALUES" % tablename)
    if _test: return sql_query
    db_cursor = self._db_cursor()
    if seqname is not False:
        sql_query = self._process_insert_query(sql_query, tablename, seqname)
    if isinstance(sql_query, tuple):
        # for some databases, a separate query has to be made to find
        # the id of the inserted row.
        q1, q2 = sql_query
        self._db_execute(db_cursor, q1)
        self._db_execute(db_cursor, q2)
    else:
        self._db_execute(db_cursor, sql_query)
    try:
        out = db_cursor.fetchone()[0]
    except Exception:
        out = None
    if not self.ctx.transactions:
        self.ctx.commit()
    return out

def insert_ignore(self, tablename, seqname=None, _test=False, **values): 
    """
    Inserts `values` into `tablename`. Returns current sequence ID.
    Set `seqname` to the ID if it's not the default, or to `False`
    if there isn't one.
        >>> db = DB(None, {})
        >>> q = db.insert('foo', name='bob', age=2, created=SQLLiteral('NOW()'), _test=True)
        >>> q
        <sql: "REPLACE INTO foo (age, name, created) VALUES (2, 'bob', NOW())">
        >>> q.query()
        'REPLACE INTO foo (age, name, created) VALUES (%s, %s, NOW())'
        >>> q.values()
        [2, 'bob']
    """
    def q(x): return "(" + x + ")"
    if values:
        _keys = SQLQuery.join(values.keys(), '`,`',prefix='`', suffix='`')
        _values = SQLQuery.join([sqlparam(v) for v in values.values()], ', ')
        sql_query = "INSERT IGNORE INTO %s " % tablename + q(_keys) + ' VALUES ' + q(_values)
    else:
        sql_query = SQLQuery("INSERT IGNORE INTO %s DEFAULT VALUES" % tablename)
    if _test: return sql_query
    db_cursor = self._db_cursor()
    if seqname is not False:
        sql_query = self._process_insert_query(sql_query, tablename, seqname)
    if isinstance(sql_query, tuple):
        # for some databases, a separate query has to be made to find
        # the id of the inserted row.
        q1, q2 = sql_query
        self._db_execute(db_cursor, q1)
        self._db_execute(db_cursor, q2)
    else:
        self._db_execute(db_cursor, sql_query)
    try:
        out = db_cursor.fetchone()[0]
    except Exception:
        out = None
    if not self.ctx.transactions:
        self.ctx.commit()
    return out

def multiple_replace(self, tablename, values, seqname=None, _test=False):
    """
    Inserts multiple rows into `tablename`. The `values` must be a list of dictioanries,
    one for each row to be inserted, each with the same set of keys.
    Returns the list of ids of the inserted rows.
    Set `seqname` to the ID if it's not the default, or to `False`
    if there isn't one.
        >>> db = DB(None, {})
        >>> db.supports_multiple_insert = True
        >>> values = [{"name": "foo", "email": "foo@example.com"}, {"name": "bar", "email": "bar@example.com"}]
        >>> db.multiple_insert('person', values=values, _test=True)
        <sql: "REPLACE INTO person (name, email) VALUES ('foo', 'foo@example.com'), ('bar', 'bar@example.com')">
    """
    if not values:
        return []
    if not self.supports_multiple_insert:
        out = [self.r_insert(tablename, seqname=seqname, _test=_test, **v) for v in values]
        if seqname is False:
            return None
        else:
            return out
    keys = values[0].keys()
    #@@ make sure all keys are valid

    # make sure all rows have same keys.
    for v in values:
        if v.keys() != keys:
            raise ValueError, 'Bad data'

    sql_query = SQLQuery('REPLACE INTO %s (%s) VALUES ' % (tablename, SQLQuery.join(keys, '`,`',prefix='`', suffix='`'))) 

    data = []
    for row in values:
        d = SQLQuery.join([SQLParam(row[k]) for k in keys], ', ')
        data.append('(' + d + ')')
    sql_query += SQLQuery.join(data, ', ')

    if _test: return sql_query

    db_cursor = self._db_cursor()
    if seqname is not False: 
        sql_query = self._process_insert_query(sql_query, tablename, seqname)

    if isinstance(sql_query, tuple):
        # for some databases, a separate query has to be made to find 
        # the id of the inserted row.
        q1, q2 = sql_query
        self._db_execute(db_cursor, q1)
        self._db_execute(db_cursor, q2)
    else:
        self._db_execute(db_cursor, sql_query)

    try: 
        out = db_cursor.fetchone()[0]
        out = range(out-len(values)+1, out+1)        
    except Exception: 
        out = None

    if not self.ctx.transactions: 
        self.ctx.commit()
    return out

def multiple_insert_ignore(self, tablename, values, seqname=None, _test=False):
    """
    Inserts multiple rows into `tablename`. The `values` must be a list of dictioanries,
    one for each row to be inserted, each with the same set of keys.
    Returns the list of ids of the inserted rows.
    Set `seqname` to the ID if it's not the default, or to `False`
    if there isn't one.
        >>> db = DB(None, {})
        >>> db.supports_multiple_insert = True
        >>> values = [{"name": "foo", "email": "foo@example.com"}, {"name": "bar", "email": "bar@example.com"}]
        >>> db.multiple_insert('person', values=values, _test=True)
        <sql: "REPLACE INTO person (name, email) VALUES ('foo', 'foo@example.com'), ('bar', 'bar@example.com')">
    """
    if not values:
        return []
    if not self.supports_multiple_insert:
        out = [self.r_insert(tablename, seqname=seqname, _test=_test, **v) for v in values]
        if seqname is False:
            return None
        else:
            return out
    keys = values[0].keys()
    #@@ make sure all keys are valid

    # make sure all rows have same keys.
    for v in values:
        if v.keys() != keys:
            raise ValueError, 'Bad data'

    sql_query = SQLQuery('INSERT IGNORE INTO %s (%s) VALUES ' % (tablename, SQLQuery.join(keys, '`,`',prefix='`', suffix='`'))) 

    data = []
    for row in values:
        d = SQLQuery.join([SQLParam(row[k]) for k in keys], ', ')
        data.append('(' + d + ')')
    sql_query += SQLQuery.join(data, ', ')

    if _test: return sql_query

    db_cursor = self._db_cursor()
    if seqname is not False: 
        sql_query = self._process_insert_query(sql_query, tablename, seqname)

    if isinstance(sql_query, tuple):
        # for some databases, a separate query has to be made to find 
        # the id of the inserted row.
        q1, q2 = sql_query
        self._db_execute(db_cursor, q1)
        self._db_execute(db_cursor, q2)
    else:
        self._db_execute(db_cursor, sql_query)

    try: 
        out = db_cursor.fetchone()[0]
        out = range(out-len(values)+1, out+1)        
    except Exception: 
        out = None

    if not self.ctx.transactions: 
        self.ctx.commit()
    return out
