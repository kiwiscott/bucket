from bucket.core import registry
from bucket.core.errors import TenantNotFoundError, AccessKeyNotValidError, BucketItemNotFoundError
from functools import wraps


def _ensure_tenant_and_validate(tenant_, access_key):
    """validate the access keys for this tenant"""
    tenant_data = registry.TENANT_DATA_GATEWAY
    tenant = tenant_data.tenant_by_name(tenant_)
    if tenant is None:
        raise TenantNotFoundError(
            "Tenant not found error. tenant='{}', access_key='{}'".format(
                tenant_, access_key))

    if not tenant.has_access_key(access_key):
        raise AccessKeyNotValidError(
            "The access key is not valid. tenant='{}', access_key='{}'".format(
                tenant_, access_key))

    return tenant


def access_key_and_tenant_required(f):
    """
    validates access to the tenant

    REQUIRES that arg 0 of the calling function contains an object with the following 
    fields (tenant (str), access_key(str)) 
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        tenant = _ensure_tenant_and_validate(args[0].tenant,
                                             args[0].access_key)

        kwargs['tenant'] = tenant
        return f(*args, **kwargs)
    return wrapper


def access_to_bucket_required(f):
    """
    validates access to the bucket for the given fields. 

    REQUIRES that arg 0 of the calling function contains an object with the following 
    fields (tenant (str), access_key(str), bucket(str)) 
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        tenant = _ensure_tenant_and_validate(args[0].tenant,
                                             args[0].access_key)
        bucket = tenant.get_bucket(args[0].bucket)
        kwargs['bucket'] = bucket
        return f(*args, **kwargs)
    return wrapper
