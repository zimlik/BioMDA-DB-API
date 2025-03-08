# -*- encoding: utf-8 -*-
# @File: utilities.py

import hashlib

def row_to_dict(tbl, sql):
    row2dict = [{column.name: getattr(row, column.name) for column in
                 tbl.__table__.columns} for row in sql]
    return row2dict

def string2md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    md5_digest = md5.hexdigest()
    return md5_digest