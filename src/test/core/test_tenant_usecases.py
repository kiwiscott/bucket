from datetime import datetime, timedelta

import pytest

from bucket.core.entities import Tenant
from bucket.core.usecases import *
from .util import MockTenantData, build_tenant
from bucket.core import registry


@pytest.fixture
def good_access_key():
    tenants = [
        build_tenant('scott1', 'b1', 'b2'),
        build_tenant('scott2', 'b1', 'b2')
    ]

    mtd = MockTenantData(tenants)
    registry.TENANT_DATA_GATEWAY = mtd
    t = tenants[0]
    key = list(t.access_keys)[0]
    good_access_key = TenantAccessKey(t.name, key)
    return good_access_key


def test_new_tenant(good_access_key):
    t = new_tenant('Bob')
    assert t.name == 'Bob'
    # new tenants should have no buckets
    assert len(t.buckets) is 0
    # new tenants should have an default access key
    assert len(t.access_keys) is 1


def test_new_tenant_can_be_retrieved(good_access_key):
    t = new_tenant('Bob_New')
    access_key = TenantAccessKey(t.name, t.access_keys[0])
    tenant_name = tenant_name_by_access_key(access_key)
    assert tenant_name.name == 'Bob_New'


def test_good_tenant(good_access_key):
    tenant_name = tenant_name_by_access_key(good_access_key)
    assert tenant_name.name == good_access_key.name


def test_tenant_not_exists(good_access_key):
    access_key = TenantAccessKey('not_exists', 'bad_key')
    with pytest.raises(TenantNotFoundError) as excinfo:
        tenant_name_by_access_key(access_key)
    assert str(
        excinfo.value) == "Tenant not found error: TenantAccessKey(name='not_exists', access_key='bad_key')"


def test_tenant_bad_key(good_access_key):
    access_key = TenantAccessKey('scott1', 'bad_key')
    with pytest.raises(AccessKeyNotValidError) as excinfo:
        tenant_name_by_access_key(access_key)
    assert str(
        excinfo.value) == "The access key is not valid this tenant: TenantAccessKey(name='scott1', access_key='bad_key')"


def test_all_tenants(good_access_key):
    tenant = list(all_tenants())
    assert len(tenant) == 2
    assert tenant[0].name == 'scott1'
    assert tenant[0].buckets == ['b1', 'b2']
    assert tenant[1].name == 'scott2'
    assert tenant[1].buckets == ['b1', 'b2']


def test_new_bucket_for_tenant(good_access_key):
    tenant_info = new_bucket_for_tenant(good_access_key, BucketKey('a_bucket'))
    assert 'a_bucket' in tenant_info.buckets
