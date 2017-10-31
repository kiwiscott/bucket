from collections import namedtuple
from .gateways import TenantDataGateway, BucketDataGateway
from .entities import Tenant

#Input output tuples 
TenantAccessKey = namedtuple('TenantAccessKey', 'name, access_key')
BucketAccessKey = namedtuple('BucketAccessKey', 'tenant_name, access_key, bucket')

TenantName = namedtuple('TenantName', 'name')
TenantInfo = namedtuple('TenantName', 'name, access_keys, buckets')
BucketItem = namedtuple('BucketItem', 'bucket_name key data')
BucketItemKey = namedtuple('BucketItemKey', 'bucket_name key')

BucketKey = namedtuple('BucketKey', 'name')


def _ensure_tenant_and_validate(tenant_data: TenantDataGateway , tenant_access_key : TenantAccessKey):
    tenant = tenant_data.tenant_by_name(tenant_access_key.name)
    if tenant is None:
        raise TenantNotFoundError("Tenant not found error: {}".format(tenant_access_key))
    if not tenant.has_access_key(tenant_access_key.access_key):
        raise AccessKeyNotValidError("The access key is not valid this tenant: {}".format(tenant_access_key))

    return tenant


class BucketService(object):
    def __init__(self, bucket_data : BucketDataGateway) -> None:
        self.bucket_data = bucket_data
    
    def add_item(self, bucket_access_key : BucketAccessKey, bucket_item : BucketItem):
        bucket = self._bucket_must_exist_with_access(bucket_access_key)
        item = bucket.prepare_item(bucket_item.key, bucket_item.data)
        self.bucket_data.add(item)
    
    def remove_item(self, bucket_access_key : BucketAccessKey,bucket_item_key : BucketItemKey):
        bucket = self._bucket_must_exist_with_access(bucket_access_key)
        self.bucket_data.remove(bucket.id, bucket_item_key.key)

    def item(self, bucket_access_key : BucketAccessKey,bucket_item_key : BucketItemKey):
        bucket = self._bucket_must_exist_with_access(bucket_access_key)
        item = self.bucket_data.item(bucket.id, bucket_item_key.key)
        bi = self._bucket_item(bucket.name, item)
        return bi 


    def all(self, bucket_access_key: BucketAccessKey,bucket_item_key : BucketItemKey):
        bucket = self._bucket_must_exist_with_access(bucket_access_key)
        for item in self.bucket_data.all(bucket.id):
            bi = self._bucket_item(bucket.name, item)
            yield(bi)
    
    def _bucket_must_exist_with_access(bucket_access_key: BucketAccessKey):
        tenant_access_key =TenantAccessKey(bucket_access_key.tenant_name,bucket_access_key.access_key) 
        tenant = _ensure_tenant_and_validate(self.tenant_data,tenant_acess_key)
        bucket = tenant.get_bucket(bucket_item.bucket_name)

        
    def _bucket_item(self, bucket_name, item):
        return BucketItem(bucket_name,item.key, item.data)

   
class TenantService(object):
    def __init__(self, tenant_data : TenantDataGateway) -> None:
        self.tenant_data = tenant_data
    
    def new_tenant(self, name):
        tenant = Tenant(name)
        tenant.new_access_key()
        self.tenant_data.save(tenant)
        return self._tenant_to_tenant_info(tenant)

    def tenant_name_by_access_key(self, tenant_access_key : TenantAccessKey):
        tenant = _ensure_tenant_and_validate(self.tenant_data, tenant_access_key)
        return TenantName(name=tenant.name)

    def new_bucket_for_tenant(self, tenant_access_key : TenantAccessKey,bucket_key :BucketKey) -> None:
        tenant = _ensure_tenant_and_validate(self.tenant_data, tenant_access_key)
        tenant.new_bucket(bucket_key.name)
        self.tenant_data.save(tenant)
        return self._tenant_to_tenant_info(tenant)

    def new_access_key(self, tenant_access_key : TenantAccessKey) -> None:
        tenant = _ensure_tenant_and_validate(self.tenant_data, tenant_access_key)
        return tenant.new_access_key()

    def all_tenants(self):
        for tenant in self.tenant_data.find_all():
            ti = self._tenant_to_tenant_info(tenant)
            yield(ti)
        return None

    def _tenant_to_tenant_info(self, tenant): 
        buckets = list(tenant.buckets)
        return TenantInfo(name = tenant.name,
            access_keys =  list(tenant.access_keys),buckets = buckets)


class TenantNotFoundError(Exception):
    """Raised when a tenant is invalid"""
    pass

class AccessKeyNotValidError(Exception):
    """Raised when a tenant / acess key combination is invalid"""
    pass

class DuplicateBucketKeyError(Exception):
    """Raised when a bucket key already exists for a tenant"""
    pass