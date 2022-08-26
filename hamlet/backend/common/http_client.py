from httpx import Client, Timeout


class HTTPClient(Client):
    """
    A standard httpx client used in the hamlet cli
    """

    def __init__(
        self,
        *args,
        http1: bool = True,
        http2: bool = True,
        timeout: Timeout(timeout=5.0, read=120.0),
        follow_redirects: bool = True,
        trust_env: bool = True,
        **kwargs
    ):
        super().__init__(
            *args, http1, http2, timeout, follow_redirects, trust_env, **kwargs
        )
