import pytest
import src.server.custom_types as ct
import src.server.http_requests as hreq


@pytest.fixture
def get_request_with_body() -> str:
    return '''GET /blog/posts/1234 HTTP/1.1
Host: www.google.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Content-Type: text/html; charset=UTF-8
Content-Length: 345

{
    'field1': 'value1',
    'field2': 'value2'
}
'''


def test_parse_request(get_request_with_body):
    parsed_request: ct.HttpRequestDetails = hreq.parse_request(get_request_with_body)
    assert parsed_request.request_method == 'GET'
    assert parsed_request.request_path == '/blog/posts/1234'
    assert 'ver_major' in parsed_request.http_version
    assert parsed_request.http_version['ver_major'] == 1
    assert 'ver_minor' in parsed_request.http_version
    assert parsed_request.http_version['ver_minor'] == 1
