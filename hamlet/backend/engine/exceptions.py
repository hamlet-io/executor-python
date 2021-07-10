from hamlet.backend.common.exceptions import BackendException


class HamletEngineInvalidVersion(BackendException):
    """
    Raise when the engine found in state does not align with the version the cli supports
    """

    def __init__(self, engine_name, version):
        self.version = version
        self.engine_name = engine_name

        msg = (
            f"Engine {self.engine_name} state not supported by this cli version"
            f"- run: hamlet engine install-engine {self.engine_name}"
        )
        super().__init__(msg)


class EngineStoreException(BackendException):
    """
    A base exception for issues in the Engine Store
    """

    pass


class EngineStoreMissingEngineException(EngineStoreException):
    """
    A requested engine can't be found in the engine store
    """

    pass
