"""Common units."""


def Time():
    """Time units."""
Time.MIN = lambda n: n * 60
Time.HOUR = lambda n: n * 3600
Time.DAY = lambda n: n * 3600 * 24


def DataSize():
    """DataSize units."""
DataSize.KB = lambda n: n * 1024
DataSize.MB = lambda n: n * 1024 * 1024
DataSize.GB = lambda n: n * 1024 * 1024 * 1024
DataSize.TB = lambda n: n * 1024 * 1024 * 1024 * 1024
