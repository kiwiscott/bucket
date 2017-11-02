from datetime import datetime, timedelta

import pytest

from bucket.core.entities import Tenant
from bucket.usecase import *
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
    assert t.tenant == 'Bob'
    # new tenants should have no buckets
    assert len(t.buckets) is 0
    # new tenants should have an default access key
    assert len(t.access_keys) is 1


def test_new_tenant_can_be_retrieved(good_access_key):
    t = new_tenant('Bob_New')
    access_key = TenantAccessKey(t.tenant, t.access_keys[0])
    tenant_name = tenant_by_access_key(access_key)
    assert tenant_name.tenant == 'Bob_New'


def test_good_tenant(good_access_key):
    tenant_name = (good_access_key)
    assert tenant_name.tenant == good_access_key.tenant


def test_tenant_not_exists(good_access_key):
    access_key = TenantAccessKey('not_exists', 'bad_key_x')
    with pytest.raises(TenantNotFoundError) as excinfo:
        tenant_by_access_key(access_key)
    assert str(
        excinfo.value) == "Tenant not found error. tenant='not_exists', access_key='bad_key_x'"


def test_tenant_bad_key(good_access_key):
    access_key = TenantAccessKey('scott1', 'bad_key')
    with pytest.raises(AccessKeyNotValidError) as excinfo:
        tenant_by_access_key(access_key)
    assert str(
        excinfo.value) == "The access key is not valid. tenant='scott1', access_key='bad_key'"


def test_all_tenants(good_access_key):
    tenant = list(all_tenants())
    assert len(tenant) == 2
    assert tenant[0].tenant == 'scott1'
    assert tenant[0].buckets == ['b1', 'b2']
    assert tenant[1].tenant == 'scott2'
    assert tenant[1].buckets == ['b1', 'b2']


def test_new_bucket_for_tenant(good_access_key):
    bak2 = BucketAccessKey(good_access_key.tenant, good_access_key.access_key, 'a_bucket')

    tenant_info = new_bucket_for_tenant(bak2)
    assert 'a_bucket' in tenant_info.buckets
