#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import random
from apipool.stats import StatsCollector, StatusCollection
from apipool.tests import GoogleMapApiKey, apikeys
from sqlalchemy_mate import engine_creator


@pytest.fixture()
def collector():
    engine = engine_creator.create_sqlite()
    collector = StatsCollector(engine=engine)
    collector.add_all_apikey(
        [GoogleMapApiKey(apikey=apikey) for apikey in apikeys]
    )

    status_id_list = StatusCollection.get_id_list()
    for _ in range(100):
        primary_key = random.choice(apikeys)
        status_id = random.choice(status_id_list)
        collector.add_event(primary_key, status_id)
    return collector


class TestDashboardQuery(object):
    def test_usage_count_in_recent_n_seconds(self, collector):
        assert collector.usage_count_in_recent_n_seconds(3600) == 100

        assert sum([
            collector.usage_count_in_recent_n_seconds(3600, primary_key=key)
            for key in apikeys
        ]) == 100

        assert sum([
            collector.usage_count_in_recent_n_seconds(
                3600, status_id=status_id)
            for status_id in StatusCollection.get_id_list()
        ]) == 100

    def test_usage_count_stats_in_recent_n_seconds(self, collector):
        stats = collector.usage_count_stats_in_recent_n_seconds(3600)
        assert sum(list(stats.values()))


class TestDashboardConstructor(object):
    def test(self):
        engine = engine_creator.create_sqlite()
        collector = StatsCollector(engine=engine)
        assert len(collector._cache_apikey) == 0
        collector.add_all_apikey(
            [GoogleMapApiKey(apikey=apikey) for apikey in apikeys]
        )
        assert len(collector._cache_apikey) == 4


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
