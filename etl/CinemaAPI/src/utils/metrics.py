from typing import Callable
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Counter


def http_requested_languages_total() -> Callable[[Info], None]:
    METRIC = Counter(
        "http_requested_languages_total",
        "Number of times a certain language has been requested.",
        labelnames=("langs",)
    )

    def instrumentation(info: Info) -> None:
        langs = set()
        lang_str = info.request.headers.get("Accept-Language", 'None')
        for element in lang_str.split(","):
            element = element.split(";")[0].strip().lower()
            langs.add(element)
        for language in langs:
            METRIC.labels(language).inc()

    return instrumentation

def request_limit_exceeded() -> Callable[[Info], None]:
    METRIC = Counter(
        "http_request_limit_exceeded",
        "Number of times request limit exceeded",
    )
    def instrumentation(info: Info) -> None:
        status = info.response.status_code
        if status == 429:
            METRIC.inc()

    return instrumentation
