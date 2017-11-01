
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