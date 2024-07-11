import pytest
import _pytest.fixtures as Fixtures
import src.server.custom_types as ct
import src.server.http_requests as hreq

# TODO: Add failing tests


@pytest.fixture
def get_headers() -> list[str]:
    return [
        'Host',
        'User-Agent',
        'Accept',
        'Accept-Language',
        'Accept-Encoding',
        'Connection',
        'Upgrade-Insecure-Requests',
        'Content-Type',
        'Content-Length',
    ]


@pytest.fixture
def get_request_no_body() -> str:
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
'''


@pytest.fixture
def get_request_with_multiline_body() -> str:
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
    "field1": "value1",
    "field2": "value2"
}
'''


@pytest.fixture
def get_request_with_single_line_body() -> str:
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

{"field1": "value1", "field2": "value2"}
'''


def test_parse_request_line(get_request_no_body: str) -> None:
    parsed_request: ct.HttpRequestDetails = hreq.parse_request(get_request_no_body)
    assert parsed_request.request_method == 'GET'
    assert parsed_request.request_path == '/blog/posts/1234'
    assert 'ver_major' in parsed_request.http_version
    assert parsed_request.http_version['ver_major'] == 1
    assert 'ver_minor' in parsed_request.http_version
    assert parsed_request.http_version['ver_minor'] == 1


def test_parse_request_headers(get_headers: list[str], get_request_no_body: str) -> None:
    parsed_request: ct.HttpRequestDetails = hreq.parse_request(get_request_no_body)
    assert len(parsed_request.headers) == 9
    assert get_headers == list(parsed_request.headers.keys())
    assert parsed_request.headers['Host'] == 'www.google.com'
    assert (parsed_request.headers['User-Agent'] ==
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0')
    assert parsed_request.headers['Accept'] == 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    assert parsed_request.headers['Accept-Language'] == 'en-US,en;q=0.5'
    assert parsed_request.headers['Accept-Encoding'] == 'gzip, deflate'
    assert parsed_request.headers['Connection'] == 'keep-alive'
    assert parsed_request.headers['Upgrade-Insecure-Requests'] == '1'
    assert parsed_request.headers['Content-Type'] == 'text/html; charset=UTF-8'
    assert parsed_request.headers['Content-Length'] == '345'


def test_parse_request_no_body_is_none(get_request_no_body: str) -> None:
    parsed_request: ct.HttpRequestDetails = hreq.parse_request(get_request_no_body)
    assert parsed_request.body is None


@pytest.mark.parametrize(
    'req_name',
    [
        pytest.param('get_request_with_multiline_body'),
        pytest.param('get_request_with_single_line_body'),
    ],
)
def test_parse_request_multiline_body(req_name: str, request: Fixtures.FixtureRequest) -> None:
    req = request.getfixturevalue(req_name)
    parsed_request: ct.HttpRequestDetails = hreq.parse_request(req)
    assert parsed_request.body is not None
    assert isinstance(parsed_request.body, dict)
    assert len(parsed_request.body) == 2
    assert parsed_request.body['field1'] == 'value1'
    assert parsed_request.body['field2'] == 'value2'
