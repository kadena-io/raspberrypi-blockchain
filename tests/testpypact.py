import unittest
from datetime import datetime

from pypact import BasePactAdapter
from pypact import api


class TestPyPact(unittest.TestCase):
    def test_update_temp_humidity(self):
        kwargs = {
            "temp": 35.5, "humidity": 45.5,
            "keyset_name": "admin-keyset",
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        code = BasePactAdapter.build_code(
            "raspberrypi", "update-temp-humidity",
            "admin-keyset", **kwargs
        )
        print(api.send_and_listen(code, "admin-keyset"))


if __name__ == '__main__':
    unittest.main()
