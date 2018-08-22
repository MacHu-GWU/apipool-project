#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..apikey import ApiKey


class ReachLimitError(Exception):
    pass


class GoogleMapApiClient(object):
    def __init__(self, apikey):
        self.apikey = apikey

    def get_lat_lng_by_address(self, address):
        return {"lat": 40.762882, "lng": -73.973700}

    def raise_other_error(self, address):
        raise ValueError

    def raise_reach_limit_error(self, address):
        raise ReachLimitError


class GoogleMapApiKey(ApiKey):
    def __init__(self, apikey):
        self.apikey = apikey

    def user_01_get_primary_key(self):
        return self.apikey

    def user_02_create_client(self):
        return GoogleMapApiClient(self.apikey)

    def user_03_test_usable(self, client):
        if "99" in self.apikey:
            return False
        response = client.get_lat_lng_by_address(
            "123 North St, NewYork, NY 10001")
        if ("lat" in response) and ("lng" in response):
            return True
        else:
            return False


apikeys = [
    "example1@gmail.com",
    "example2@gmail.com",
    "example3@gmail.com",
    "example99@gmail.com",
]
