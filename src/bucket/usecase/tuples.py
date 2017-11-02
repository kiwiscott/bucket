from typing import NamedTuple, List


# Output Tuples
class TenantInfo(NamedTuple):
    """"Information about a current Tenants Configuraion"""
    tenant: str
    access_keys: List[str]
    buckets: List[str]

class ItemInfo(NamedTuple):
    """Item data information tuple"""
    bucket: str
    item_key:  str
    data: bytes

#Input Tuples
class TenantAccessKey(NamedTuple):
    """Access Key for a tenant"""
    tenant: str
    access_key:  str

class BucketAccessKey(NamedTuple):
    """buckets access information"""
    tenant: str
    access_key:  str
    bucket: str

class BucketItemKey(NamedTuple):
    """access information for a bucket item"""
    tenant: str
    access_key:  str
    bucket: str
    item_key: str

class BucketItem(NamedTuple):
    """add a new bucket item"""
    tenant: str
    access_key:  str
    bucket: str
    item_key: str
    data: bytes
