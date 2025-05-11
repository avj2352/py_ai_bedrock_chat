"""
    environment variables
    defined here
"""
import os

def _get_aws_access_key_id():
    return os.environ.get("AWS_ACCESS_KEY_ID") or ""

def _get_aws_secret_access_key():
    return os.environ.get("AWS_SECRET_ACCESS_KEY") or "" 


def _get_aws_region():
    return os.environ.get("AWS_REGION") or "us-east-1"


AWS_ACCESS_KEY_ID = _get_aws_access_key_id()
AWS_SECRET_ACCESS_KEY = _get_aws_secret_access_key()
AWS_REGION = _get_aws_region()
