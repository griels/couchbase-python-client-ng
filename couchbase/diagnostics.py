from abc import abstractmethod
from typing import Optional, Mapping, Union, Any
from enum import Enum
from couchbase_core import JSON


class ServiceType(Enum):
    View = "view"
    KeyValue = "kv"
    Query = "n1ql"
    Search = "fts"
    Analytics = "cbas"
    Config = "config"


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
                 service_type,  # type: Union[ServiceType,str]
                 raw_endpoint  # type: JSON
                 ):
        self._raw_endpoint = raw_endpoint
        if isinstance(service_type, ServiceType):
            self._service_type = service_type
        else:
            try:
                self._service_type = ServiceType(service_type)
            except:
                self._service_type = service_type

    def type(self):
        # type: (...)->Union[ServiceType,str]
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
                 source_diagnostics  # type: Mapping[str,Any]
                 ):
        self._src_diagnostics = source_diagnostics

    def id(self):
        # type: (...)->str
        return self._src_diagnostics.get('id')

    def version(self):
        # type: (...)->int
        return self._src_diagnostics.get('version')

    def sdk(self):
        # type: (...)->str
        return self._src_diagnostics.get('sdk')

    def services(self):
        # type: (...)->Mapping[str, IEndPointDiagnostics]
        return self._src_diagnostics.get('services', {})
