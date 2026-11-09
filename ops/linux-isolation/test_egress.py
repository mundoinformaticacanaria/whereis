import socket
import unittest
from egress import endpoint, public_pins


def records(*addresses):
    return lambda *_args, **_kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (address, 443)) for address in addresses]


class EgressTests(unittest.TestCase):
    def test_approved_tls_only(self):
        self.assertEqual(endpoint('https://api.github.com/'), 'api.github.com')
        for value in ['http://api.github.com', 'https://api.github.com:444', 'https://user@api.github.com',
                      'https://api.github.com.evil.invalid', 'https://127.0.0.1', 'https://openrouter.ai@localhost',
                      'https://api.github.com/#fragment']:
            with self.subTest(value=value), self.assertRaises(ValueError): endpoint(value)

    def test_public_pin(self):
        self.assertEqual(public_pins('api.github.com', records('8.8.8.8')), '8.8.8.8')

    def test_private_special_and_mixed_dns_fail_closed(self):
        for address in ['127.0.0.1','10.1.2.3','172.16.0.1','192.168.0.1','169.254.169.254',
                        '100.64.0.1','0.0.0.0','::1','fe80::1','fc00::1','::ffff:127.0.0.1',
                        '224.0.0.1','240.0.0.1','255.255.255.255','198.18.0.1','192.0.2.1']:
            with self.subTest(address=address), self.assertRaises(ValueError):
                public_pins('api.github.com', records('8.8.8.8',address))

    def test_empty_dns_rejected(self):
        with self.assertRaises(ValueError):public_pins('api.github.com', records())

    def test_unapproved_not_resolved(self):
        def resolver(*_args,**_kwargs):raise AssertionError('Must not resolve')
        with self.assertRaises(ValueError):public_pins('example.invalid', resolver)


if __name__ == '__main__':unittest.main()
