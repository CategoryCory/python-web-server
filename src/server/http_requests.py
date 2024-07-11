import custom_types
import exceptions
import json

http_methods: list[str] = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


def parse_request(req: str) -> custom_types.HttpRequestDetails:
    """
    Parses an HTTP request and returns a HttpRequestDetails object.

    :param req: The HTTP request to parse.
    :type req: str
    :return: An HttpRequestDetails object containing the parsed data.
    :rtype: custom_types.HttpRequestDetails
    :raises exceptions.HttpRequestError: If the request is not well-formed.
    """
    req_lines: list[str] = req.splitlines()
    empty_line_index: int = (next((i for i, line in enumerate(req_lines) if line.strip() == ""), len(req_lines))
                             if '' in req_lines
                             else -1)

    # Parse request line
    request_line: list[str] = req_lines[0].split(' ')
    if len(request_line) != 3:
        raise exceptions.HttpRequestException('Invalid request header length')

    # Get HTTP method
    http_method: str = request_line[0]
    if http_method not in http_methods:
        raise exceptions.HttpRequestException('Invalid HTTP method')

    # Get path
    path: str = request_line[1]

    # Get version
    if not request_line[2].startswith('HTTP/'):
        raise exceptions.HttpRequestException('Invalid HTTP version')

    slash_position: int = request_line[2].find('/')

    version_parts: list[str] = request_line[2][slash_position + 1:].split('.')
    if len(version_parts) != 2:
        raise exceptions.HttpRequestException('Invalid HTTP version')

    version_dict: dict[str, int] = {
        'ver_major': int(version_parts[0]),
        'ver_minor': int(version_parts[1]),
    }

    # Get headers
    headers_dict: dict[str, str] = {}
    stop_line: int = len(req_lines) if empty_line_index == -1 else empty_line_index - 1
    header_parts: list[list[str]] = [line.split(':', 1) for line in req_lines[1:stop_line]]
    for hdr_part in header_parts:
        if len(hdr_part) != 2:
            raise exceptions.HttpRequestException('Invalid header format')

        headers_dict[hdr_part[0]] = hdr_part[1].strip()

    # Get body, if exists
    parsed_body = None
    if empty_line_index != -1:
        try:
            req_body = ''.join([line.replace('\'', '"').strip() for line in req_lines[stop_line + 2:]])
            parsed_body = json.loads(req_body)
        except json.decoder.JSONDecodeError:
            raise exceptions.HttpRequestException('Invalid JSON body')

    return custom_types.HttpRequestDetails(http_method, path, version_dict, headers_dict, parsed_body)
