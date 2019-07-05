from abc import abstractmethod
from enum import IntEnum
from typing import Optional, Mapping

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
        # type: (...)->Optional[int]
        pass

    @abstractmethod
    def scope(self):
        # type: (...)-Optional[>str]
        pass


class IDiagnosticsResult:
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
                 service_type,  # type: str
                 raw_endpoint  # type: JSON
                 ):
        self._raw_endpoint = raw_endpoint
        self._service_type = service_type

    def type(self):
        # type: (...)->ServiceType
        return self._service_type

    def id(self):
        # type: (...)->str
        return self._raw_endpoint.get('id')

    def local(self):
        # type: (...)->str
        return self._raw_endpoint.get('local')

    def remote(self):
        # type: (...)->str
        return self._raw_endpoint.get('remote')

    def last_activity(self):
        # type: (...)->int
        return self._raw_endpoint.get('last_activity_us')

    def latency(self):
        # type: (...)->Optional[int]
        return self._raw_endpoint.get('latency')

    def scope(self):
        # type: (...)->str
        return self._raw_endpoint.get('scope')


class DiagnosticsResult(IDiagnosticsResult):
    def __init__(self,  # type: DiagnosticsResult
                 raw_diagnostics  # type: JSON
                 ):
        self._raw_diagnostics = raw_diagnostics

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
        return self._raw_diagnostics.get('services', {})
