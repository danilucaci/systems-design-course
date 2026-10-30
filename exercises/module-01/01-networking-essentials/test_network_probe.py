import unittest
from unittest.mock import patch, MagicMock
from network_probe import probe


class NetworkingTests(unittest.TestCase):
    def test_rejects_unsafe_or_unsupported_url_shapes(self):
        for url in ('http://example.com', 'https://user:pass@example.com', 'https://example.com/#x', 'file:///tmp/x'):
            with self.subTest(url=url), self.assertRaises(ValueError): probe(url)

    @patch('network_probe.socket.getaddrinfo', return_value=[(2, 1, 6, '', ('127.0.0.1', 443))])
    @patch('network_probe.http.client.HTTPSConnection')
    def test_closes_connection_and_limits_body_read(self, factory, lookup):
        connection = factory.return_value
        response = connection.getresponse.return_value
        response.status = 200
        response.read.return_value = b'ok'
        self.assertEqual(probe('https://example.com/a?q=1')['sample_bytes'], 2)
        connection.request.assert_called_once_with('GET', '/a?q=1')
        response.read.assert_called_once_with(4096)
        connection.close.assert_called_once()

    @patch('network_probe.socket.getaddrinfo', return_value=[])
    @patch('network_probe.http.client.HTTPSConnection')
    def test_connect_failure_still_releases_socket(self, factory, lookup):
        factory.return_value.connect.side_effect = TimeoutError('test timeout')
        with self.assertRaises(TimeoutError): probe('https://example.com')
        factory.return_value.close.assert_called_once()
