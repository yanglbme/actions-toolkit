import asyncio
import errno
import logging
import os
import platform
import re
from functools import wraps, partial
from pathlib import Path
from stat import S_ISDIR

from typing import List

IS_WINDOWS = platform.system() == 'Windows'


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        p = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, p)

    return run


stat = wrap(os.stat)

lstat = wrap(os.lstat)
rename = wrap(os.rename)
remove = wrap(os.remove)
mkdir = wrap(os.mkdir)
rmdir = wrap(os.rmdir)

if hasattr(os, "sendfile"):
    sendfile = wrap(os.sendfile)


async def exists(fs_path: str):
    try:
        await stat(fs_path)
    except IOError as e:
        if e.errno == errno.ENOENT:
            return False
        raise e
    return True


async def is_directory(fs_path: str, use_stat: bool = False):
    stats = await stat(fs_path) if use_stat else await lstat(fs_path)
    return S_ISDIR(stats.st_mode)


async def is_rooted(p: str) -> bool:
    p = normalize_separators(p)
    if not p:
        raise Exception('is_rooted() parameter "p" cannot be empty')

    if IS_WINDOWS:
        return p.startswith('\\') or re.match(r'^[A-Z]', p, re.IGNORECASE) is not None
    return p.startswith('/')


async def mkdir_p(fs_path: str, max_depth: int = 1000, depth: int = 1):
    if not fs_path:
        raise Exception('a path argument must be provided')
    fs_path = Path(fs_path).resolve()
    if depth >= max_depth:
        return mkdir(fs_path)

    try:
        await mkdir(fs_path)
        return
    except IOError as e:
        if e.errno == errno.ENOENT:
            await mkdir_p(str(fs_path), max_depth, depth + 1)
            await mkdir(fs_path)
            return
        try:
            stats = await stat(fs_path)
        except Exception as e2:
            raise e2
        if not S_ISDIR(stats.st_mode):
            raise e


async def try_get_executable_path(file_path: str, extensions: List[str]):
    stats = None
    try:
        stats = await stat(file_path)
    except IOError as e:
        if e.errno != errno.ENOENT:
            logging.log(f'Unexpected error attempting to determine if executable file exists "{file_path}": {e}')
    if stats and Path(file_path).is_file():
        if IS_WINDOWS:
            upper_ext = Path(file_path).suffix.upper()
            for valid_ext in extensions:
                if valid_ext.upper() == upper_ext:
                    return file_path
        else:
            if is_unix_executable(file_path):
                return file_path
    return ''


def normalize_separators(p: str) -> str:
    return os.path.normpath(p or '')


def is_unix_executable(file_path) -> bool:
    return os.access(file_path, os.X_OK)
