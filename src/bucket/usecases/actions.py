from bucket.core import registry
from bucket.core.entities import Tenant

from bucket.core .errors import (AccessKeyNotValidError, BucketItemNotFoundError,
                     TenantNotFoundError)
from .security import access_key_and_tenant_required, access_to_bucket_required
from .tuples import (BucketAccessKey, BucketItem, BucketItemKey, ItemInfo,
                     TenantAccessKey, TenantInfo)



#@must_be_secured
def new_tenant(name):
    tenant = Tenant(name)
    tenant.new_access_key()
    registry.TENANT_DATA_GATEWAY.save(tenant)
    ti = TenantInfo(tenant=tenant.name,
                    access_keys=list(tenant.access_keys),
                    buckets=list(tenant.buckets))

    return ti

#@must_be_secured
def all_tenants():
    for tenant in registry.TENANT_DATA_GATEWAY.find_all():
        ti = TenantInfo(tenant=tenant.name,
                        access_keys=list(tenant.access_keys),
                        buckets=list(tenant.buckets))
        yield(ti)
    return None



@access_key_and_tenant_required
def new_bucket_for_tenant(bucket_access_key: BucketAccessKey, **kwargs) -> TenantInfo:
    tenant = kwargs['tenant']
    tenant.new_bucket(bucket_access_key.bucket)
    registry.TENANT_DATA_GATEWAY.save(tenant)
    return TenantInfo(tenant=tenant.name,
                      access_keys=list(tenant.access_keys),
                      buckets=list(tenant.buckets))



@access_key_and_tenant_required
def tenant_by_access_key(tenant_access_key: TenantAccessKey, *args, **kwargs):
    tenant = kwargs['tenant']
    ti = TenantInfo(tenant=tenant.name,
                    access_keys=list(tenant.access_keys),
                    buckets=list(tenant.buckets))
    return ti


@access_to_bucket_required
def add_item_to_bucket(bucket_item, **kwargs):
    bucket = kwargs['bucket']
    item = bucket.prepare_item(bucket_item.item_key, bucket_item.data)
    registry.BUCKET_DATA_GATEWAY.save(item)


@access_to_bucket_required
def remove_item_from_bucket(bucket_item_key, **kwargs):
    bucket = kwargs['bucket']
    registry.BUCKET_DATA_GATEWAY.delete(bucket.id, bucket_item_key.item_key)



@access_to_bucket_required
def item_in_bucket(bucket_item_key, **kwargs):
    bucket = kwargs['bucket']
    item = registry.BUCKET_DATA_GATEWAY.one_in_bucket(
        bucket.id, bucket_item_key.item_key)
    if item is None:
        raise BucketItemNotFoundError("Bucket Item could not be found bucket='{}' "
                                      "key='{}'".format(bucket.key, bucket_item_key.item_key))
    bi = ItemInfo(bucket.key, item.key, item.data)
    return bi


@access_to_bucket_required
def all_items_in_bucket(bucket_access_key: BucketAccessKey, **kwargs) -> ItemInfo:
    bucket = kwargs['bucket']
    for item in registry.BUCKET_DATA_GATEWAY.all_in_bucket(bucket.id):
        bi = ItemInfo(bucket.key, item.key, item.data)
        yield(bi)
