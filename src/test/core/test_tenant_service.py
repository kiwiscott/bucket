from datetime import datetime, timedelta

import pytest

from bucket.core.entities import Tenant
from bucket.core.services import *
from .util import MockTenantData

class TestTenantService(object):
    @pytest.fixture
    def tenant_setup(self):
        tenants = [
            self._tenant('scott1', 'b1', 'b2'),
            self._tenant('scott2', 'b1', 'b2')
        ]
        mtd = MockTenantData(tenants)
        ts = TenantService(mtd)
        return ts,tenants

    def test_new_tenant(self):
        mtd = MockTenantData([])
        ts = TenantService(mtd)
        t = ts.new_tenant('Bob')
        assert t.name == 'Bob'
        #new tenants should have no buckets
        assert len(t.buckets) is 0
        #new tenants should have an default access key
        assert len(t.access_keys) is 1

    def test_new_tenant_can_be_retrieved(self):
        mtd = MockTenantData([])
        ts = TenantService(mtd)
        t = ts.new_tenant('Bob')
        access_key = TenantAccessKey (t.name, t.access_keys[0])
        tenant_name = ts.tenant_name_by_access_key(access_key)
        assert tenant_name.name == 'Bob'

    def test_good_tenant(self,tenant_setup):
        tenant_service, tenants = tenant_setup

        tenant = tenants[0]
        name = tenants[0].name
        access_key = list(tenant.access_keys)[0]

        access_key = TenantAccessKey (name, access_key)
        tenant_name = tenant_service.tenant_name_by_access_key(access_key)
        assert tenant_name.name == name

    def test_tenant_not_exists(self,tenant_setup):
        tenant_service, tenants = tenant_setup

        access_key = TenantAccessKey ('not_exists', 'bad_key')
        with pytest.raises(TenantNotFoundError) as excinfo:
            tenant_service.tenant_name_by_access_key(access_key)
        assert str(excinfo.value) == "Tenant not found error: TenantAccessKey(name='not_exists', access_key='bad_key')"

    def test_tenant_bad_key(self,tenant_setup):
        tenant_service, tenants = tenant_setup

        access_key = TenantAccessKey ('scott1', 'bad_key')
        with pytest.raises(AccessKeyNotValidError) as excinfo:
            tenant_service.tenant_name_by_access_key(access_key)
        assert str(excinfo.value) == "The access key is not valid this tenant: TenantAccessKey(name='scott1', access_key='bad_key')"


    def test_all_tenants(self,tenant_setup):
        tenant_service, tenants = tenant_setup
        tenant = list(tenant_service.all_tenants())
        assert len(tenant) == 2 
        assert tenant[0].name == 'scott1'
        assert tenant[0].buckets == ['b1','b2'] 
        assert tenant[1].name == 'scott2'
        assert tenant[1].buckets == ['b1','b2']

    def test_new_bucket_for_tenant(self,tenant_setup):
        tenant_service, tenants = tenant_setup

        tenant = tenants[0]
        name = tenants[0].name
        access_key = list(tenant.access_keys)[0]
        tenant_info = tenant_service.new_bucket_for_tenant(TenantAccessKey (name, access_key),
            BucketKey('a_bucket'))
        assert 'a_bucket' in tenant_info.buckets


    def _tenant(self, name, *buckets):
        t = Tenant(name)
        for bucket in buckets:
            t.new_bucket(bucket)
        for key in range(2):
            t.new_access_key()
        return t