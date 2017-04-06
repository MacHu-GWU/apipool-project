#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .base import GenericData, ExceptionHavingDefaultMessage
except:
    from apipool.base import GenericData, ExceptionHavingDefaultMessage
    
    
import sys
import random
import pprint
from collections import OrderedDict


class NoAvailableAPIError(ExceptionHavingDefaultMessage):
    """Raised when there's no API Key is usable.
    """
    default_message = "Run out of all API keys!"


class BaseApiKeyNotWorkingError(ExceptionHavingDefaultMessage):
    """Raised when API Key is not working, and not a Exceed Quota Error.
    """
    default_message = "This api key is not working!"


class BaseApiKey(GenericData):

    """An api key may have: access key, secret key, ... and arbitrary many
    information.

    :params primary_key: :class:`BaseApiKey` can have arbitary many attributes, 
      but there's only one is the primary_key. Please specify.
    :params _api_manager: is bind to the :class:`APIManager` instance.
    :params _client: a variable bind to the client actually using this api key.
      self._client is the object doing real api call.
    """
    _primary_key = None
    _api_manager = None
    _client = None
    __excludes__ = ["_primary_key", "_api_manager", "_client"]
    
    def create_client(self, *args, **kwargs):
        """A method that create an api client instance.
        
        **中文文档**
        
        定义此方法, 用此Api Key创建一个Api Client。
        """
        raise NotImplementedError
        client = ApiClient(self.api_key)
        return client
    
    @property
    def client(self):
        return self._client
    
    def bind_client(self, *args, **kwargs):
        """Bind this key with it's api client.
        """
        self._client = self.create_client()

    def is_working(self, *args, **kwargs):
        """A method return True or False to indicate that if this API Key is 
        usable. Usually, it consumes one API quota.

        :returns flag: True, False
        """
        raise NotImplementedError
        flag = False
        return flag

    def get_primary_key(self):
        """Get the value of it's primary_key.
        """
        return getattr(self, self._primary_key)


class APIManager(object):

    """API manager holds collection of :class:`BaseApiKey`. And 

    :param apikey_pool: list of :class:`BaseApiKey`
    :attr key_chain: ordered ``{apikey.primary_key: apikey}`` mapping
    :attr archived_key_chain：
    :param used_counter: counts of how many time each api key been used.
    """
    def __init__(self, apikey_pool):
        self.key_chain = OrderedDict()
        self.archived_key_chain = OrderedDict()
        self.used_counter = dict()

        for api_key in apikey_pool:
            api_key.bind_client()
            key = api_key.get_primary_key()
            self.key_chain[key] = api_key
            self.used_counter[key] = 0

    def fetch_one(self):
        """Populate one api key from the key chain. If there's no api key 
        available.
        """
        try:
            return self.key_chain[random.choice(list(self.key_chain))]
        except IndexError:
            raise NoAvailableAPIError

    def remove_one(self, key):
        self.archived_key_chain[key] = self.key_chain.pop(key)
    
    @property
    def client(self):
        return self.fetch_one().client
    
    def check_usable(self):
        for key, apikey in self.key_chain.items():
            if not apikey.is_working():
                self.remove_one(key)

        if len(self.key_chain) == 0:
            sys.stderr.write("\nThere's no API Key usable!")
        elif len(self.archived_key_chain) == 0:
            sys.stderr.write("\nAll API Key are usable.")
        else:
            sys.stderr.write("\nThese keys are not usable:")
            for key in self.archived_key_chain:
                sys.stderr.write("\n    %s: %r" % (key, apikey))

    def __repr__(self):
        return pprint.pformat(list(self.key_chain.items()))
    

#--- Unittest ---
if __name__ == "__main__":
    from geopy.geocoders import GoogleV3
    from geopy.exc import GeocoderQuotaExceeded
    
    def test_APIManager():
        class MyApiKey(BaseApiKey):
            _primary_key = "key"
        
        api_manager = APIManager(apikey_pool=[
            MyApiKey(key="a"), MyApiKey(key="b"), MyApiKey(key="c"),
        ])
        api_manager.remove_one("a")
        assert "a" not in api_manager.key_chain
        assert "a" in api_manager.archived_key_chain
        
#     test_APIManager()
    
    # Implementation
    class GoogleGeocodeApiKey(BaseApiKey):
        _primary_key = "key"
    
        def __init__(self, key):
            self.key = key
    
        def create_client(self, *args, **kwargs):
            return GoogleV3(self.key)
    
        def is_working(self):
            # The White House
            address = "1600 Pennsylvania Ave NW, Washington, DC 20500"
            expect_formatted_address = "1600 Pennsylvania Ave NW, Washington, DC 20500, USA"
    
            location = self.client.geocode(address, exactly_one=True)
            formatted_address = location.raw["formatted_address"]
            if formatted_address in expect_formatted_address:
                return True
            else:
                # raise BaseApiKeyNotWorkingError
                sys.stderr.write("\nOutput is %r doesn't match %r!" %
                                 (formatted_address, expect_formatted_address))
                return False
    
    
    # Usage
    def test():
        GOOGLE_API_KEYS = [
            "AIzaSyAuzs8xdbysdYZO1wNV3vVw1AdzbL_Dnpk",  # Sanhe 01
            "AIzaSyBhO6ocH1qfg1zD-bJaptpHy5UWpZxL2iQ",  # Sanhe 02
            "AIzaSyDCNOTxBjrQn12K6XsRykRJCophmL0I91g",  # Sanhe 03
            "AIzaSyDkYgBX_Fi7Jop3IP3ZDMOHJqphCrYxuqs",  # Sanhe 04
            "AIzaSyDlTwtO17n1daw8FMTV_HM0hP4T1FnutyM",  # Sanhe 05
        ]
        
        apikey_pool = list()
        for key in GOOGLE_API_KEYS:
            apikey = GoogleGeocodeApiKey(key)
            apikey_pool.append(apikey)
        
        api_manager = APIManager(apikey_pool=apikey_pool)
        api_manager.check_usable()
        
        # Put many address here
        task = [
            "3120 Kenni Ln Dunkirk, MD 20754",
        ]
        
        # Doing some real work
        for todo in task:
            try:
                # do geocoding, call the client method.
                location = api_manager.client.geocode(task, exactly_one=True)
                if location:
                    pprint.pprint(location.raw)
                else:
                    pass
            except GeocoderQuotaExceeded:
                # this key is no longer usable
                api_manager.remove_one(apikey.key)
            except Exception as e:
                print(repr(e))
    
    test()