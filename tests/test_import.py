#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import apipool

    apipool.ApiKey
    apipool.ApiKeyManager
    apipool.StatusCollection


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
