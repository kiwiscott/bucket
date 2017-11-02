import uuid
import base64
import datetime
from .errors import BucketItemNotFoundError, DuplicateBucketKeyError


class Item(object):
    """
    A bucket contains items. 
    TTL input is in seconds. Items are automatically removed after the requested amount of time has expired.
    Any subsequent update of the column resets the TTL to the TTL specified in the update. 
    By default, values never expire.
    """

    def __init__(self, bucket_id, key, data, changed=None,  ttl_seconds=None) -> None:
        assert key is not None and data is not None, \
            "key and data must not be None"

        self.bucket_id = bucket_id
        self.key = key
        self.data = data
        self.ttl_seconds = ttl_seconds
        self.changed = changed if changed else datetime.datetime.utcnow()


class Bucket(object):
    """
    A bucket represents a holder for items. The actual items are associated to the bucket
    are stored as items with a reference to the bucket by id 
    """

    def __init__(self, key: str, id: str) -> None:
        self.key = key
        self.id = id

    def prepare_item(self, key : str, data : bytes, created:datetime=None,  ttl_seconds:int=None) -> Item:
        i = Item(self.id, key, data, created, ttl_seconds)
        return i


class Tenant(object):
    """
    Tenants represent a customer who owns buckets. A tenant can have one or more access keys and 
    one of more buckets. 
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.access_keys = set()
        self.buckets = {}

    def new_access_key(self) -> str:
        key = _generate_psuedo_random_key()
        self.access_keys.add(key)
        return key

    def has_access_key(self, key : str) -> bool:
        return key in self.access_keys

    def has_bucket(self, key: str) -> bool:
        return key in self.buckets

    def get_bucket(self, key : str) ->Bucket:
        if key not in self.buckets:
            raise BucketItemNotFoundError(
                "A bucket named '{}' does not exist for this tenant".format(key))
        return self.buckets[key]

    def new_bucket(self, key : str) -> Bucket:
        if key in self.buckets:
            raise DuplicateBucketKeyError(
                "A bucket named '{}' already exists for this tenant".format(key))

        id = _generate_psuedo_random_key()
        bucket = Bucket(key, id)

        self.buckets[key] = bucket
        return bucket


def _generate_psuedo_random_key():
    """produces a file safe str key using a uuid and base64 encoding"""
    id = base64.b64encode(uuid.uuid4().bytes, altchars=b'-_')
    return id
