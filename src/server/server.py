import custom_types
import http_requests


def run_server() -> None:
    print('Server starting...')

    test_request: str = '''GET /blog/posts/1234 HTTP/1.1
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

    # print(test_request)
    parsed_request: custom_types.HttpRequestDetails = http_requests.parse_request(test_request)
    print(parsed_request)


if __name__ == '__main__':
    run_server()
