import dataclasses


@dataclasses.dataclass(frozen=True)
class HttpRequestDetails:
    """
    A class to represent the details of an HTTP request.

    Attributes
    ----------
    request_method: str
        The method of the request.
    request_path: str
        The path of the request.
    http_version: dict[str, int]
        The HTTP version of the request.
    headers: dict[str, str]
        The headers of the request.
    body: dict[str, str] | None
        The body of the request, if any; None otherwise.
    """
    request_method: str
    request_path: str
    http_version: dict[str, int]
    headers: dict[str, str]
    body: dict[str, str] | None = None


@dataclasses.dataclass(frozen=True)
class HttpResponseDetails:
    pass
