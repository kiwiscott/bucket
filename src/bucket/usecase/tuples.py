from typing import NamedTuple, List


# Output Tuples
class TenantInfo(NamedTuple):
    """Information about a tenant."""
    tenant: str
    access_keys: List[str]
    buckets: List[str]

class ItemInfo(NamedTuple):
    """Information about a tenant."""
    bucket: str
    item_key:  str
    data: bytes

#Input Tuples
class TenantAccessKey(NamedTuple):
    """Information about a tenant."""
    tenant: str
    access_key:  str

class BucketAccessKey(NamedTuple):
    tenant: str
    access_key:  str
    bucket: str

class BucketItemKey(NamedTuple):
    tenant: str
    access_key:  str
    bucket: str
    item_key: str

class BucketItem(NamedTuple):
    tenant: str
    access_key:  str
    bucket: str
    item_key: str
    data: bytes
