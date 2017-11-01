from collections import namedtuple
from .gateways import TenantDataGateway, BucketDataGateway
from .entities import Tenant
from . import registry

# Input output tuples
TenantAccessKey = namedtuple('TenantAccessKey', 'name, access_key')
BucketAccessKey = namedtuple(
    'BucketAccessKey', 'tenant_name, access_key, bucket')
TenantName = namedtuple('TenantName', 'name')
TenantInfo = namedtuple('TenantName', 'name, access_keys, buckets')
BucketItem = namedtuple('BucketItem', 'bucket_name key data')
BucketItemKey = namedtuple('BucketItemKey', 'key')
BucketKey = namedtuple('BucketKey', 'name')


def _ensure_tenant_and_validate(tenant_data: TenantDataGateway, tenant_access_key: TenantAccessKey):
    tenant = tenant_data.tenant_by_name(tenant_access_key.name)
    if tenant is None:
        raise TenantNotFoundError(
            "Tenant not found error: {}".format(tenant_access_key))
    if not tenant.has_access_key(tenant_access_key.access_key):
        raise AccessKeyNotValidError(
            "The access key is not valid this tenant: {}".format(tenant_access_key))

    return tenant


def access_key_and_tenant_required(fn):
    def _check(tenant_access_key, *args, **kwargs):
        tenant_data = registry.TENANT_DATA_GATEWAY
        tenant = tenant_data.tenant_by_name(tenant_access_key.name)
        if tenant is None:
            raise TenantNotFoundError(
                "Tenant not found error: {}".format(tenant_access_key))
        if not tenant.has_access_key(tenant_access_key.access_key):
            raise AccessKeyNotValidError(
                "The access key is not valid this tenant: {}".format(tenant_access_key))
        return fn(tenant, *args, **kwargs)
    return _check


def access_to_bucket_required(fn):
    def _check(bucket_access_key, *args, **kwargs):
        tenant_access_key = TenantAccessKey(
            bucket_access_key.tenant_name, bucket_access_key.access_key)
        tenant = _ensure_tenant_and_validate(
            registry.TENANT_DATA_GATEWAY, tenant_access_key)
        bucket = tenant.get_bucket(bucket_access_key.bucket)
        return fn(bucket, *args, **kwargs)
    return _check


@access_key_and_tenant_required
def new_bucket_for_tenant(tenant, bucket_key: BucketKey):
    tenant.new_bucket(bucket_key.name)
    registry.TENANT_DATA_GATEWAY.save(tenant)
    return TenantInfo(name=tenant.name,
                      access_keys=list(tenant.access_keys),
                      buckets=list(tenant.buckets))


@access_key_and_tenant_required
def tenant_name_by_access_key(tenant):
    return TenantName(name=tenant.name)


#@must_be_secured
def all_tenants():
    for tenant in registry.TENANT_DATA_GATEWAY.find_all():
        ti = TenantInfo(name=tenant.name,
                        access_keys=list(tenant.access_keys),
                        buckets=list(tenant.buckets))
        yield(ti)
    return None

#@must_be_secured


def new_tenant(name):
    tenant = Tenant(name)
    tenant.new_access_key()
    registry.TENANT_DATA_GATEWAY.save(tenant)
    ti = TenantInfo(name=tenant.name,
                    access_keys=list(tenant.access_keys),
                    buckets=list(tenant.buckets))

    return ti


@access_to_bucket_required
def add_item_to_bucket(bucket, bucket_item):
    item = bucket.prepare_item(bucket_item.key, bucket_item.data)
    registry.BUCKET_DATA_GATEWAY.save(item)


@access_to_bucket_required
def remove_item_from_bucket(bucket, bucket_item_key):
    registry.BUCKET_DATA_GATEWAY.delete(bucket.id, bucket_item_key.key)


@access_to_bucket_required
def item_in_bucket(bucket, bucket_item_key):
    item = registry.BUCKET_DATA_GATEWAY.one_in_bucket(
        bucket.id, bucket_item_key.key)
    if item is None:
        raise BucketItemNotFoundError("Bucket Item could not be found bucket='{}' "
                                      "key='{}'".format(bucket.key, bucket_item_key.key))
    bi = BucketItem(bucket.key, item.key, item.data)
    return bi


@access_to_bucket_required
def all_items_in_bucket(bucket):
    for item in registry.BUCKET_DATA_GATEWAY.all_in_bucket(bucket.id):
        bi = BucketItem(bucket.key, item.key, item.data)
        yield(bi)


class BucketItemNotFoundError(Exception):
    """Raised when a bucket item is not found"""
    pass


class TenantNotFoundError(Exception):
    """Raised when a tenant is invalid"""
    pass


class AccessKeyNotValidError(Exception):
    """Raised when a tenant / acess key combination is invalid"""
    pass


class DuplicateBucketKeyError(Exception):
    """Raised when a bucket key already exists for a tenant"""
    pass
