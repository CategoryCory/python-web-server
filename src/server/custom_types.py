import dataclasses


@dataclasses.dataclass(frozen=True)
class HttpRequestDetails:
    request_method: str
    request_path: str
    http_version: dict[str, int]
    headers: dict[str, str]
    body: dict[str, str] | None = None


@dataclasses.dataclass(frozen=True)
class HttpResponseDetails:
    pass
