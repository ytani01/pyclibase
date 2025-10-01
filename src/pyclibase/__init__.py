#
# (c) 2025 Yoichi Tanibayashi
#
from importlib.metadata import version as get_version

from .pyclibase import CliBase

if __package__:
    __version__ = get_version(__package__)
else:
    __version__ = "_._._"


__all__ = [
    "__version__",
    "CliBase",
]
