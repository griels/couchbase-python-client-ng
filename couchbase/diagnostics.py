from abc import abstractmethod
from enum import IntEnum

from couchbase_core import CompatibilityEnum, JSONMapping


class ServiceTypeRaw(CompatibilityEnum):
    @classmethod
    def prefix(cls):
        return "LCB_PING_SERVICE_"

    KV = ()
    VIEWS = ()
    N1QL = ()
    FTS = ()
    ANALYTICS = ()


class ServiceType(IntEnum):
    View = ServiceTypeRaw.VIEWS
    KeyValue = ServiceTypeRaw.KV
    Query = ServiceTypeRaw.N1QL
    Search = ServiceTypeRaw.FTS
    Analytics = ServiceTypeRaw.ANALYTICS


class IEndPointDiagnostics:
    @abstractmethod
    def type(self):
        # type: (...)->ServiceType
        pass

    @abstractmethod
    def id(self):
        # type: (...)->str
        pass

    @abstractmethod
    def local(self):
        # type: (...)->str
        pass

    @abstractmethod
    def remote(self):
        # type: (...)->str
        pass

    @abstractmethod
    def last_activity(self):
        # type: (...)->int
        pass

    @abstractmethod
    def latency(self):
        # type: (...)->int
        pass

    @abstractmethod
    def scope(self):
        # type: (...)->str
        pass


class IDiagnosticResult:
    @abstractmethod
    def id(self):
        # type: (...)->str
        pass

    @abstractmethod
    def version(self):
        # type: (...)->int
        pass

    @abstractmethod
    def sdk(self):
        # type: (...)->str
        pass

    @abstractmethod
    def services(self):
        # type: (...)->Mapping[str, IEndPointDiagnostics]
        pass


class EndPointDiagnostics(IEndPointDiagnostics):
    def __init__(self,  # type: EndPointDiagnostics
                 raw_endpoint  # type: JSON
                 ):
        self.raw_endpoint = raw_endpoint

    def type(self):
        # type: (...)->ServiceType
        pass

    def id(self):
        # type: (...)->str
        pass

    def local(self):
        # type: (...)->str
        pass

    def remote(self):
        # type: (...)->str
        pass

    def last_activity(self):
        # type: (...)->int
        pass

    def latency(self):
        # type: (...)->int
        pass

    def scope(self):
        # type: (...)->str
        pass


class DiagnosticsResult(IDiagnosticResult, JSONMapping):
    def __init__(self,  # type: DiagnosticsResult
                 raw_diagnostics  # type: JSON
                 ):
        super(DiagnosticsResult, self).__init__(raw_diagnostics)
        self._services = {k: EndPointDiagnostics(v) for k, v in raw_diagnostics.get('services', {})}

    def id(self):
        # type: (...)->str
        return self._raw_diagnostics.get('id')

    def version(self):
        # type: (...)->int
        return self._raw_diagnostics.get('version')

    def sdk(self):
        # type: (...)->str
        return self._raw_diagnostics.get('sdk')

    def services(self):
        # type: (...)->Mapping[str, IEndPointDiagnostics]
        return self._services