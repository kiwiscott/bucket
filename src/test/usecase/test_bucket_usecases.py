from datetime import datetime, timedelta

import pytest

from bucket.core.entities import Tenant
from bucket.usecase import *
from bucket.core import registry

from .util import MockTenantData, MockBucketData, build_tenant


@pytest.fixture
def setup_bucket_key():
    tenants = [
        build_tenant('scott1', 'b1', 'b2'),
        build_tenant('scott2', 'b1', 'b2')
    ]

    mtd = MockTenantData(tenants)
    mbd = MockBucketData([])

    registry.BUCKET_DATA_GATEWAY = mbd
    registry.TENANT_DATA_GATEWAY = mtd

    t = tenants[0]
    key = list(t.access_keys)[0]
    bucket_key = BucketAccessKey(t.name, key, 'b1')

    return bucket_key


def test_add_item_to_bucket(setup_bucket_key):
    bucket_item = BucketItem(setup_bucket_key.tenant, setup_bucket_key.access_key,'b1', 'an_item', 'data data data data')
    add_item_to_bucket(bucket_item)

    # validate the item added
    k = BucketItemKey(setup_bucket_key.tenant, setup_bucket_key.access_key,'b1', 'an_item')
    i = item_in_bucket(k)
    assert i.data == bucket_item.data


def test_add_2000_items_then_get(setup_bucket_key):
    for i in range(2000):
        bucket_item = BucketItem(
            setup_bucket_key.tenant, setup_bucket_key.access_key,
            'b1', 'an_item_{}'.format(i), 'data data data data')
        add_item_to_bucket(bucket_item)

    # validate the item added
    assert len(list(all_items_in_bucket(setup_bucket_key))) == 2000


def test_add_delete(setup_bucket_key):
 
    bucket_item = BucketItem(setup_bucket_key.tenant, setup_bucket_key.access_key,  'b1', 'an_item', 'data data data data')
    add_item_to_bucket(bucket_item)
    # delete
    k = BucketItemKey(setup_bucket_key.tenant, setup_bucket_key.access_key,'b1', 'an_item')
    remove_item_from_bucket(k)
    # error on read
    with pytest.raises(BucketItemNotFoundError) as excinfo:
        item_in_bucket(k)

    error_expected = "Bucket Item could not be found bucket='{1}' key='{2}'".format(
        setup_bucket_key.tenant, setup_bucket_key.bucket, bucket_item.item_key)
    assert str(excinfo.value) == error_expected
