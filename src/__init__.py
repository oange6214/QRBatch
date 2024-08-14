from importlib.metadata import version

try:
    __version__ = version("excel-qr-generator")
except:
    __version__ = "unknown"