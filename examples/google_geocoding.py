#!/usr/bin/env python
# -*- coding: utf-8 -*-


from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQuotaExceeded

from apipool import ApiKey, ApiKeyManager


class GoogleGeocoderApiKey(ApiKey):
    def __init__(self, apikey):
        self.apikey = apikey

    def user_01_get_primary_key(self):
        return self.apikey

    def user_02_create_client(self):
        return GoogleV3(self.apikey)

    def user_03_test_usable(self, client):
        address = "1600 Pennsylvania Ave NW, Washington, DC 20500"
        expect_formatted_address = "1600 Pennsylvania Ave NW, Washington, DC 20500, USA"

        location = client.geocode(address, exactly_one=True)
        formatted_address = location.raw["formatted_address"]
        if formatted_address in expect_formatted_address:
            return True
        else:
            return False


if __name__ == "__main__":
    from windtalker import SymmtricCipher

    apikeys = [
        "Z0FBQUFBQmJmSTN1cnlFY3owcFNLb0x0RHhBbTZhVXpiTEpIbGZjS2tRMGpMdDg4V3hyMXJMMXU5a0ZXS09VTVhybnlZTmZZS2I3d2U0TDJYcWtldENaVl91cGhBeGZRN3R6aWlKUTZtZEpPTGdKNlhpNy13UG9ieVNDOHYyRHhtaFlQMmpydHBJdEk =",
        "Z0FBQUFBQmJmSTN1S0ZaWXVTeDNFczczMFNxNGtLcnpxbzhHZmFhMVhpazBwZTVZZlJyWU4ybEtxQ3RKSEs1ZDBYU2txajNrWl9nWEZRMk1OeWItZk55cG8yZ0hkMk9VZDV3REZSNFlQQnlucmVULVlIRjNEYkZIbU9qQmw5S2pRcVRtRTFRMjBQeTY =",
        "Z0FBQUFBQmJmSTN1aF82QklRdDdTS01LTlZ2emN3TkplY0RWc1dfSzIyTlF0YnY5TXVSZ2VWSjNVUmsxS1dPTmVMT29Dcjc0NFV5R2JGa09nQjN0QS1jU3piT1BRc2NGa1hPd3E0R2NZbVp1RmFMUVAwd0hpaU5ZQ1VRWnhyN3hFcGdacUJycTQ2Wmg =",
        "Z0FBQUFBQmJmSTN1VXFfUEF6Vi1CNUVHaEZZVUdwdFhPMDBLa2kybmxaVWNiblM0aUs1UVhFWFY4anM3d2VLN19sdzQyNi0yQkxZRlRTODF1Nmd0aDBmTzhwVnRZdWNqOHRicUhYZ2EwRV9PRGdTN3dWTV92LVpNYXRCeHZRREM5ZDVRcF90aFQzd2o =",
        "Z0FBQUFBQmJmSTN1S0FPdER6V2JSVGRkSldaUDJfS1V6WEJUZzcxbndhaUZ2YmNqcDZmeWgyaUE1TjF3VDFSZUJiX2xxSGppWExKLUtqTXZjUTlDeTQtcTFRYUtrY1Z4N0MxMHphTmEwWWhJR1ZfWnpDdmdtY212dzlPSEZ3ckpmenhNMGZuYXpFZjA =",
    ]


    def create_cipher(password=None):
        try:
            input = raw_input
        except:
            pass
        if password is None:
            password = input("Please enter the password: ")
        return SymmtricCipher(password)


    cipher = create_cipher(password=None)
    apikeys = [cipher.decrypt_text(key) for key in apikeys]
    apikey_list = [GoogleGeocoderApiKey(key) for key in apikeys]

    manager = ApiKeyManager(
        apikey_list=apikey_list,
        reach_limit_exc=GeocoderQuotaExceeded,
    )
    manager.check_usable()

    address = "1600 Pennsylvania Ave NW, Washington, DC 20500"

    for _ in range(3):
        res = manager.dummyclient.geocode(address, exactly_one=True)
    print(manager.stats.usage_count_stats_in_recent_n_seconds(3600))
