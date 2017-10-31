from abc import ABC, abstractmethod
from typing import Generator

from .entities import Tenant


class BucketDataGateway(ABC):
    @abstractmethod
    def tenant_by_name(self, name) -> Tenant:
        pass

    @abstractmethod
    def find_all(self) -> Generator[Tenant,None,None]:
        pass

    @abstractmethod
    def delete(self, Tenant) -> None:
        pass

    @abstractmethod
    def save(self, Tenant) -> None:
        pass



class TenantDataGateway(ABC):
    @abstractmethod
    def tenant_by_name(self, name) -> Tenant:
        pass

    @abstractmethod
    def find_all(self) -> Generator[Tenant,None,None]:
        pass

    @abstractmethod
    def delete(self, Tenant) -> None:
        pass

    @abstractmethod
    def save(self, Tenant) -> None:
        pass
