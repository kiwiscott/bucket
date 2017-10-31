from datetime import datetime, timedelta
from typing import Generator

from bucket.core.entities import Tenant
from bucket.core.gateways import TenantDataGateway


class MockTenantData(TenantDataGateway):
    def __init__(self, tenants):
        self._tenants ={} 
        for t in tenants:
            self._tenants[t.name] = t 
        
        
    def tenant_by_name(self, name) -> Tenant:
        if name in self._tenants:
            return self._tenants[name]
        return None

    def find_all(self) -> Generator[Tenant,None,None]:
        for t in self._tenants:
            yield self._tenants[t] 
        return None

    def delete(self, Tenant) -> None:
        del self._tenants[tenant.name]

    def save(self, tenant: Tenant) -> None:
        self._tenants[tenant.name] = tenant
