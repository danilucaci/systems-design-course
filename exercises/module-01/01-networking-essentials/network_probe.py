"""Bounded HTTPS timing probe. Resolves DNS separately; connect includes a second lookup."""
import http.client
import socket
import ssl
import time
from urllib.parse import urlsplit


def probe(url: str, timeout: float = 2.0) -> dict:
    target = urlsplit(url)
    if target.scheme != 'https' or not target.hostname or target.username or target.password or target.fragment:
        raise ValueError('Use an HTTPS URL without credentials or a fragment')
    if not 0 < timeout <= 30:
        raise ValueError('timeout must be greater than zero and at most 30 seconds')
    port = target.port or 443
    start = time.monotonic()
    addresses = socket.getaddrinfo(target.hostname, port, type=socket.SOCK_STREAM)
    resolved = time.monotonic()
    connection = http.client.HTTPSConnection(target.hostname, port, timeout=timeout, context=ssl.create_default_context())
    try:
        connection.connect()
        connected = time.monotonic()
        connection.request('GET', (target.path or '/') + ('?' + target.query if target.query else ''))
        response = connection.getresponse()
        headers = time.monotonic()
        sample = response.read(4096)
        return {'addresses': len({item[4][0] for item in addresses}), 'status': response.status,
                'dns_ms': round((resolved-start)*1000, 2),
                'connect_including_tls_ms': round((connected-resolved)*1000, 2),
                'request_to_headers_ms': round((headers-connected)*1000, 2), 'sample_bytes': len(sample)}
    finally:
        connection.close()


if __name__ == '__main__':
    import json
    import sys
    print(json.dumps(probe(sys.argv[1]), indent=2))
