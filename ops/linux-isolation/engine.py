"""Declarative provider selection. No shell sourcing or credentials in the registry."""
import json
import os
from pathlib import Path
import re
import stat


def instance(path):
    values = {}
    for row in Path(path).read_text().splitlines():
        if not row.strip() or row.startswith("#"):
            continue
        key, value = row.split("=", 1)
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key) or key in values:
            raise ValueError("Invalid/duplicate instance key")
        if any(c in value for c in "\n\r\x00"):
            raise ValueError("Invalid instance value")
        values[key] = value
    return values


def selected(values, profiles):
    provider, model = values["MODEL"].split("/", 1)
    profile = profiles[provider]
    if not model or not re.fullmatch(r"[A-Z][A-Z0-9_]*", profile["credential_env"]):
        raise ValueError("Invalid model/provider profile")
    if not profile["endpoint"].startswith("https://"):
        raise ValueError("TLS endpoint required")
    if profile.get("approved") is not True:
        raise ValueError("Provider profile needs approval")
    return provider, model, profile


def registry(values, profiles, config):
    provider, model, profile = selected(values, profiles)
    result = dict(config)
    result["providers"] = {provider: {"env": [profile["credential_env"]],
                                    "package": profile["package"], "models": {model: {}}}}
    return result


def credential_environment(values, profiles, path):
    _, _, profile = selected(values, profiles)
    path = Path(path)
    meta = path.lstat()
    if not stat.S_ISREG(meta.st_mode) or meta.st_uid != os.getuid() or meta.st_nlink != 1 or meta.st_mode & 0o077:
        raise ValueError("Private exclusive credential file required")
    if any(parent.is_symlink() for parent in path.parents):
        raise ValueError("Symlink credential ancestor rejected")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(fd)
        if (opened.st_dev, opened.st_ino) != (meta.st_dev, meta.st_ino):
            raise ValueError("Credential changed during validation")
        if (not stat.S_ISREG(opened.st_mode) or opened.st_uid != os.getuid()
                or opened.st_nlink != 1 or opened.st_mode & 0o077):
            raise ValueError("Private exclusive credential file required")
        with os.fdopen(fd, "r") as stream:
            fd = -1
            data = json.load(stream)
    finally:
        if fd >= 0:
            os.close(fd)
    key = profile["credential_env"]
    if set(data) != {key} or not isinstance(data[key], str) or not data[key].strip():
        raise ValueError("Missing dedicated provider credential")
    return {key: data[key]}
