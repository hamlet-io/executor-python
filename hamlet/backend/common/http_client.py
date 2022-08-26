from httpx import Client, Timeout


class HTTPClient(Client):
    """
    A standard httpx client used in the hamlet cli
    """

    def __init__(
        self,
        *args,
        timeout=Timeout(timeout=5.0, read=120.0),
        follow_redirects: bool = True,
        trust_env: bool = True,
        **kwargs
    ):
        super().__init__(
            *args,
            timeout=timeout,
            follow_redirects=follow_redirects,
            trust_env=trust_env,
            **kwargs
        )
