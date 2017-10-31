import pytest
from bucket.core.entities import Bucket, Tenant, DuplicateBucketKeyError, BucketDoesNotExistError
from datetime import datetime, timedelta

class TestBucket(object):
    def test_create_bucket(self):
        bucket = Bucket('key', 'id')
        assert bucket.key is 'key'
        assert bucket.id is 'id'

    def test_create_item_in_bucket(self):
        bucket = Bucket('key', 'id')
        type, data = 'ikey', 123456
        item = bucket.prepare_item(type, data)

        assert item.key is 'ikey'
        assert item.bucket_id is bucket.id
        assert item.data is data

    def test_check_datetime_on_creation(self):
        bucket = Bucket('key', 'id')
        now = datetime.utcnow() - timedelta(seconds=1)
        item = bucket.prepare_item('ikey', 123456)
        assert item.changed > now

    def test_key_assertion(self):
        bucket = Bucket('key', 'id')
        with pytest.raises(AssertionError) as excinfo:
            bucket.prepare_item(None, 123456)
        assert str(excinfo.value) == "key and data must not be None"

    def test_data_assertion(self):
        bucket = Bucket('key', 'id')
        with pytest.raises(AssertionError) as excinfo:
            bucket.prepare_item('keykey', None)
        assert str(excinfo.value) == "key and data must not be None"

    def test_check_ttl(self):
        bucket = Bucket('key', 'id')
        seconds_in_one_day = 86400
        
        item = bucket.prepare_item('type', 123456, ttl_seconds = seconds_in_one_day)
        assert item.ttl_seconds is seconds_in_one_day

class TestTenant(object):
    def test_create(self):
        tenant = Tenant('scott')
        assert tenant.name is 'scott'

    def test_has_bucket(self):
        tenant = Tenant('scott')
        assert not tenant.has_bucket('default')

    def test_cannot_create_duplicate_buckets(self):
        tenant = Tenant('scott')
        tenant.new_bucket('default')
        with pytest.raises(DuplicateBucketKeyError) as excinfo:
            tenant.new_bucket('default')

        assert str(
            excinfo.value) == "A bucket named 'default' already exists for this tenant"

    def test_has_bucket_true(self):
        tenant = Tenant('scott')
        tenant.new_bucket('default')
        assert tenant.has_bucket('default')

    def test_has_access_key(self):
        tenant = Tenant('scott')
        key = tenant.new_access_key()
        assert tenant.has_access_key(key)

    def test_has_access_key_false(self):
        tenant = Tenant('scott')
        assert not tenant.has_access_key('never_exists')

    def test_get_bucket(self):
        tenant = Tenant('scott')
        b1 = tenant.new_bucket('default')
        b2 = tenant.get_bucket('default')
        assert b1 is b2

    def test_get_bucket_errors(self):
        tenant = Tenant('scott')
        with pytest.raises(BucketDoesNotExistError) as excinfo:
            tenant.get_bucket('default')

        assert str(
            excinfo.value) == "A bucket named 'default' does not exist for this tenant"
