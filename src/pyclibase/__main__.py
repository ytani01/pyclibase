#
# (c) 2025 Yoichi Tanibayashi
#
from .pyclibase import CliBase


def main():
    """test main"""
    cli = CliBase("test", "/tmp/hist", debug=True)
    cli.loop()
