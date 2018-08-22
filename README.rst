.. image:: https://travis-ci.org/MacHu-GWU/apipool-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/apipool-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/apipool-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/apipool-project

.. image:: https://img.shields.io/pypi/v/apipool.svg
    :target: https://pypi.python.org/pypi/apipool

.. image:: https://img.shields.io/pypi/l/apipool.svg
    :target: https://pypi.python.org/pypi/apipool

.. image:: https://img.shields.io/pypi/pyversions/apipool.svg
    :target: https://pypi.python.org/pypi/apipool

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/apipool-project


Welcome to ``apipool`` Documentation
==============================================================================

``apipool`` allows developer manipulate multi api key at same time. For example, if single api key has 1k/day quota, then you can register 10 api keys, and let ``apipool`` to automatically rotate the key.


**Features**:

- automatically rotate apikey.
- built-in usage statistics, easy to search by ``time``, ``status``, ``apikey``. You can deploy stats collector on any cloud relational database.
- clean api, minimal code is required to implement complex feature.


**Example**:

there's a google geocoding example at: https://github.com/MacHu-GWU/apipool-project/blob/master/examples/google_geocoding.py


**Tutorial**

Let's walk through with a twitter api example, the api client we use is ``python-twitter``: https://github.com/bear/python-twitter.

The ``python-twitter`` usage:

.. code-block:: python

    import twitter

    # create api client
    api = twitter.Api(
        consumer_key="consumer_key"z,
        consumer_secret="consumer_secret",
        access_token_key="access_token",
        access_token_secret="access_token_secret",
    )

    # make api call
    statuses = api.GetUserTimeline(screen_name="trump")


The ``apipool`` usage:

.. code-block:: python

    import twitter
    from apipool import ApiKey, ApiKeyManager

    class TwitterApiKey(ApiKey):
        def __init__(self,
                     consumer_key,
                     consumer_secret,
                     access_token_key,
                     access_token_secret)
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret
            self.access_token_key = access_token_key
            self.access_token_secret = access_token_secret

        def user_01_get_primary_key(self):
            return self.access_token_key

        def user_02_create_client(self):
            return twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=self.access_token_key,
                access_token_secret=self.access_token_secret,
            )

        def user_03_test_usable(self, client):
            statuses = client.GetUserTimeline(screen_name="trump")
            if len(statuses) >= 5:
                return True
            else:
                return False

    apikey_data_list = [
        {
            "consumer_key": xxx,
            "consumer_secret": xxx,
            "access_token_key": xxx,
            "access_token_secret": xxx,
        },
        {...},
        {...},
    ]

    apikey_list = [
        TwitterApiKey(**apikey_data)
        for apikey_data in apikey_data_list
    ]

    manager = ApiKeyManager(apikey_list=apikey_list)


**DummyClient**:

now we can use the ``manager.dummyclient`` object like how we use the ``twitter.Api()`` object. However, the apikey is automatically rotated, and usage events are also automatically recorded.

.. code-block:: python

    manager.check_usable()

    # the api key is automatically rotated under the hood
    statuses = manager.dummyclient.GetUserTimeline(screen_name="trump")

    for _ in range(10):
        manager.dummyclient.GetUserTimeline(screen_name="trump")


**StatsCollector**:

now we can use ``manager.stats`` object to access usage stats, and also query usage events.

.. code-block:: python

    >>> manager.stats.usage_count_stats_in_recent_n_seconds()
    {"xxx access_token_key": 3, "xxx access_token_key": 4, "xxx access_token_key": 3}

    >>> from apipool import StatusCollection
    >>> events_list = list(manager.stats.query_event_in_recent_n_seconds(
        n_seconds=24*3600,
        status_id=StatusCollection.c1_Success.id,
    ))
    >>> events_list
    [
        Event(apikey_id=xxx, finished_at=datetime(xxx), status_id=xxx),
        Event(...),
        ...
    ]


Quick Links
------------------------------------------------------------------------------
- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: https://apipool.readthedocs.io/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: https://apipool.readthedocs.io/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/apipool-project

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/MacHu-GWU/apipool-project/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/apipool#downloads


.. _install:

Install
------------------------------------------------------------------------------

``apipool`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install apipool

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade apipool
