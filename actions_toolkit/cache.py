import os
from typing import List

from actions_toolkit import core


class UploadOptions:
    """Options to control cache upload"""

    def __init__(self, upload_concurrency: int = 4, upload_chunk_size: int = 32 * 1024 * 1024):
        """Number of parallel cache upload"""
        self.upload_concurrency = upload_concurrency

        """Maximum chunk size in bytes for cache upload"""
        self.upload_chunk_size = upload_chunk_size


class DownloadOptions:
    """Options to control cache download"""

    def __init__(self, use_azure_sdk: bool = True, download_concurrency: int = 8, timeout_in_ms: int = 30000):
        """
        Indicates whether to use the Azure Blob SDK to download caches
        that are stored on Azure Blob Storage to improve reliability and
        performance
        """
        self.use_azure_sdk = use_azure_sdk

        """
        Number of parallel downloads (this option only applies when using
        the Azure SDK)
        """
        self.download_concurrency = download_concurrency

        """
        Maximum time for each download request, in milliseconds (this
        option only applies when using the Azure SDK)
        """
        self.timeout_in_ms = timeout_in_ms


def get_upload_options(**copy) -> UploadOptions:
    """
    Returns a copy of the upload options with defaults filled in.
    """
    result = UploadOptions(**copy)
    core.debug(f'Upload concurrency: {result.upload_concurrency}')
    core.debug(f'Upload chunk size: {result.upload_chunk_size}')
    return result


def get_download_options(**copy) -> DownloadOptions:
    """
    Returns a copy of the download options with defaults filled in.
    """
    result = DownloadOptions(**copy)
    core.debug(f'Use Azure SDK: {result.use_azure_sdk}')
    core.debug(f'Download concurrency: {result.download_concurrency}')
    core.debug(f'Request timeout (ms): {result.timeout_in_ms}')
    return result


def get_cache_api_url(resource: str) -> str:
    base_url = os.getenv('ACTIONS_CACHE_URL')
    if not base_url:
        raise Exception('Cache Service Url not found, unable to restore cache.')
    url = f'{base_url}_apis/artifactcache/{resource}'
    core.debug(f'Resource Url: {url}')
    return url


def check_paths(paths: List[str]):
    if not paths:
        raise Exception('Path Validation Error: At least one directory or file path is required')


def check_key(key: str):
    if len(key) > 512:
        raise Exception(f'Key Validation Error: {key} cannot be larger than 512 characters.')
    if ',' in key:
        raise Exception(f'Key Validation Error: {key} cannot contain commas.')


def is_feature_available() -> bool:
    return bool(os.getenv('ACTIONS_CACHE_URL'))
