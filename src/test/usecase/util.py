from datetime import datetime, timedelta
from typing import Generator

from bucket.core.entities import Tenant, Item
from bucket.core.gateways import TenantDataGateway, BucketDataGateway


def build_tenant( name, *buckets):
    t = Tenant(name)
    for bucket in buckets:
        t.new_bucket(bucket)
    for key in range(2):
        t.new_access_key()
    return t


class MockBucketData(BucketDataGateway):
    def __init__(self, items):
        self._items = items

    def one_in_bucket(self, bucket_id, key):
        for item in self._items:
            if item.bucket_id == bucket_id and item.key == key:
                return item
        return None

    def all_in_bucket(self, bucket_id):
        for item in self._items:
            if item.bucket_id == bucket_id:
                yield item

    def delete(self, bucket_id, key):
        for item in self._items:
            if item.bucket_id == bucket_id and item.key == key:
                self._items.remove(item)
                break

    def save(self, item: Item):
        self.delete(item.bucket_id, item.key)
        self._items.append(item)


class MockTenantData(TenantDataGateway):
    def __init__(self, tenants):
        self._tenants = {}
        for t in tenants:
            self._tenants[t.name] = t

    def tenant_by_name(self, name) -> Tenant:
        if name in self._tenants:
            return self._tenants[name]
        return None

    def find_all(self) -> Generator[Tenant, None, None]:
        for t in self._tenants:
            yield self._tenants[t]
        return None

    def delete(self, Tenant) -> None:
        del self._tenants[tenant.name]

    def save(self, tenant: Tenant) -> None:
        self._tenants[tenant.name] = tenant
