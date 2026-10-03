"""Consistent UTF-8 CLI output on Windows and Unix."""
import sys
def utf8_stdio():
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
