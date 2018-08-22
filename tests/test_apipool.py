#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from apipool import ApiKey, ApiKeyManager, StatusCollection
from apipool.tests import (
    ReachLimitError,
    GoogleMapApiClient,
    GoogleMapApiKey,
    apikeys,
)


class TestBaseApiKey(object):
    def test(self):
        apikey = GoogleMapApiKey(apikey="example@gmail.com")
        assert apikey.primary_key == "example@gmail.com"
        assert apikey.is_usable() is True


class TestApiKeyManager(object):
    def test(self):
        address = "123st, NewYork, NY 10001"

        manager = ApiKeyManager(
            apikey_list=[
                GoogleMapApiKey(apikey=apikey)
                for apikey in apikeys
            ],
            reach_limit_exc=ReachLimitError,
        )
        manager.check_usable()  # use each key once

        res = manager.dummyclient.get_lat_lng_by_address(
            address)  # make a call
        assert "lat" in res and "lng" in res
        assert manager.stats.usage_count_in_recent_n_seconds(3600) == 5
        assert max(
            list(manager.stats.usage_count_stats_in_recent_n_seconds(3600).values())) == 2

        # make 100 successful call
        for _ in range(100):
            manager.dummyclient.get_lat_lng_by_address(address)
        assert manager.stats.usage_count_in_recent_n_seconds(3600) == 105

        assert len(manager.apikey_chain) == 3
        assert len(manager.archived_apikey_chain) == 1

        # raise other error
        try:
            manager.dummyclient.raise_other_error(address)
        except:
            pass

        assert len(manager.apikey_chain) == 3
        assert len(manager.archived_apikey_chain) == 1

        # raise ReachLimitError
        try:
            manager.dummyclient.raise_reach_limit_error(address)
        except:
            pass

        assert len(manager.apikey_chain) == 2
        assert len(manager.archived_apikey_chain) == 2

        assert manager.stats.usage_count_in_recent_n_seconds(
            3600, status_id=StatusCollection.c5_Failed.id) == 2
        assert manager.stats.usage_count_in_recent_n_seconds(
            3600, status_id=StatusCollection.c9_ReachLimit.id) == 1


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
