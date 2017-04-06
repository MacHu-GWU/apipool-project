#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import copy
from collections import OrderedDict
from functools import total_ordering


@total_ordering
class GenericData(object):

    """nameddict base class.
    """
    __attrs__ = None
    """该属性非常重要, 定义了哪些属性被真正视为 ``attributes``, 换言之, 就是在
    :meth:`~Base.keys()`, :meth:`~Base.values()`, :meth:`~Base.items()`,
    :meth:`~Base.to_list()`, :meth:`~Base.to_dict()`, :meth:`~Base.to_OrderedDict()`,
    :meth:`~Base.to_json()`, 方法中要被包括的属性。
    """
    
    __excludes__ = []
    """在此被定义的属性将不会出现在 :meth:`~Base.items()` 中
    """
    
    __reserved__ = set(["keys", "values", "items"])

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __setattr__(self, attr, value):
        if attr in self.__reserved__:
            raise ValueError("%r is a reserved attribute name!" % attr)
        object.__setattr__(self, attr, value)

    def __repr__(self):
        kwargs = list()
        for attr, value in self.items():
            kwargs.append("%s=%r" % (attr, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(kwargs))

    def __getitem__(self, key):
        """Access attribute.
        """
        return object.__getattribute__(self, key)

    @classmethod
    def _make(cls, d):
        """Make an instance.
        """
        return cls(**d)

    def items(self):
        """items按照属性的既定顺序返回attr, value对。当 ``__attrs__`` 未指明时,
        则按照字母顺序返回。若 ``__attrs__`` 已定义时, 按照其中的顺序返回。

        当有 ``@property`` 装饰器所装饰的属性时, 若没有在 ``__attrs__`` 中定义,
        则items中不会包含它。
        """
        items = list()
        
        if self.__attrs__ is None:
            for key, value in self.__dict__.items():
                if key not in self.__excludes__:
                    items.append((key, value))
            items = list(sorted(items, key=lambda x: x[0]))
            return items
        try:
            for attr in self.__attrs__:
                if attr not in self.__excludes__:
                    try:
                        items.append((attr, copy.deepcopy(getattr(self, attr))))
                    except AttributeError:
                        items.append(
                            (attr, copy.deepcopy(self.__dict__.get(attr))))
            return items
        except:
            raise AttributeError()

    def keys(self):
        """Iterate attributes name.
        """
        return [key for key, value in self.items()]

    def values(self):
        """Iterate attributes value.
        """
        return [value for key, value in self.items()]

    def __iter__(self):
        """Iterate attributes.
        """
        if self.__attrs__ is None:
            return iter(self.keys())
        try:
            return iter(self.__attrs__)
        except:
            raise AttributeError()

    def to_list(self):
        """Export data to list. Will create a new copy for mutable attribute.
        """
        return self.keys()

    def to_dict(self):
        """Export data to dict. Will create a new copy for mutable attribute.
        """
        return dict(self.items())

    def to_OrderedDict(self):
        """Export data to OrderedDict. Will create a new copy for mutable 
        attribute.
        """
        return OrderedDict(self.items())

    def to_json(self):
        """Export data to json. If it is json serilizable.
        """
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        """Equal to.
        """
        return self.items() == other.items()

    def __lt__(self, other):
        """Less than.
        """
        for (_, value1), (_, value2) in zip(self.items(), other.items()):
            if value1 >= value2:
                return False
        return True
    
    
import sys
import traceback


def get_last_exc_info():
    """Get last raised exception, and format the error message.
    """
    exc_type, exc_value, exc_tb = sys.exc_info()
    for filename, line_num, func_name, code in traceback.extract_tb(exc_tb):
        tmp = "{exc_value.__class__.__name__}: {exc_value}, appears in '{filename}' at line {line_num} in {func_name}(), code: {code}"
        info = tmp.format(
            exc_value=exc_value,
            filename=filename,
            line_num=line_num,
            func_name=func_name,
            code=code,
        )
        return info


class ExceptionHavingDefaultMessage(Exception):

    """A Exception class with default error message.
    """
    default_message = None

    def __str__(self):
        length = len(self.args)
        if length == 0:
            if self.default_message is None:
                raise NotImplementedError("default_message is not defined!")
            else:
                return self.default_message
        elif length == 1:
            return str(self.args[0])
        else:
            return str(self.args)