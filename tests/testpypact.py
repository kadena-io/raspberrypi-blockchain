import unittest

from pypact import BasePactAdapter
from pypact import api


class TestPyPact(unittest.TestCase):
    def test_build_code(self):
        code = BasePactAdapter.build_code(
            "transfer-manager",
            "is-address-in-whitelist",
            "(read-keyset 'issuer-admin-keyset)",
            **{"address": "zehra"}
        )
        self.assertFalse(api.send_and_listen(code), "Address is in whitelist")


if __name__ == '__main__':
    unittest.main()
