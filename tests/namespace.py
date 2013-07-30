#!/usr/bin/env python

class Namespace(dict):
    '''an attribure-access dictionary'''
    def __init__(self, *args, **kvargs):
        super(dict, self).__init__(*args, **kvargs)
        # a little magic
        self.__dict__ = self

def load_ns(d, leaf_processor=lambda x: x):
    '''a recursive dict-to-Namespace loader'''
    if not isinstance(d, dict):
        return leaf_processor(d)
    ns = Namespace()
    for k, v in d.items():
        ns[k] = load_ns(v, leaf_processor)
    return ns

def locate_ns_item(ns, item):
    '''
    locate queries of the form 'a.b.c' in a Namespace instance
    tries to find longest match
    '''
    if item == '':
        # item found
        return ns

    sub_items = item.split('.')
    for list_prefix in [ sub_items[:i] for i in range(len(sub_items), 0, -1)]:
        item_prefix = '.'.join(list_prefix)
        item_suffix = '.'.join(sub_items[i:])
        print item, item_prefix, item_suffix
        if item_prefix in ns:
            return ns_locate(ns[item_prefix], item_suffix)

    # no match
    raise KeyError('item not found: %s' % item)

