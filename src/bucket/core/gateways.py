from abc import ABC, abstractmethod
from typing import Generator

from .entities import Tenant, Item


class BucketDataGateway(ABC):
    @abstractmethod
    def one_in_bucket(self,bucket_id, key) -> Item:
        pass

    @abstractmethod
    def all_in_bucket(self,bucket_id) -> Generator[Item,None,None]:
        pass

    @abstractmethod
    def delete(self, bucket_id, key) -> None:
        pass

    @abstractmethod
    def save(self, Item) -> None:
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
