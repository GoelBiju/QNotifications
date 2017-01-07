# -*- coding: utf-8 -*-
""" A set of functions to abstract processes for the QNotifications module. """

import sys
# from qtpy import QtCore

# Handle the types used in Python 3+ and version lower than 3.
if sys.version_info >= (3, 0, 0):
    py3 = True
    basestring = str
    universal_newline_mode = u'r'
else:
    bytes = str
    str = unicode
    py3 = False
    universal_newline_mode = u'rU'


def safe_decode(s, enc='utf-8', errors='strict'):
    """


    :param s:
    :param enc:
    :param errors:
    :return str(s):
    """
    if isinstance(s, str):
        return s
    if isinstance(s, bytes):
        return s.decode(enc, errors)
    # Numeric values are encoded right away.
    if isinstance(s, int) or isinstance(s, float):
        return str(s)
    # Some types need to be converted to unicode, but require the encoding
    # and errors parameters. Notable examples are Exceptions, which have
    # strange characters under some locales, such as French. It even appears
    # that, at least in some cases, they have to be encodeed to str first.
    # Presumably, there is a better way to do this, but for now this at
    # least gives sensible results.
    try:
        return safe_decode(bytes(s), enc=enc, errors=errors)
    except Exception:
        # print(ex)
        pass
    # For other types, the unicode representation doesn't require a specific
    # encoding. This mostly applies to non-stringy things, such as integers.
    return str(s)


def safe_encode(s, enc='utf-8', errors='strict'):
    """


    :param s:
    :param enc:
    :param errors:
    :return s.encode:
    """
    if isinstance(s, bytes):
        return s
    return s.encode(enc, errors)


if py3:
    safe_str = safe_decode
else:
    safe_str = safe_encode

__all__ = [
    'py3',
    'safe_decode',
    'safe_encode',
    'safe_str',
    'universal_newline_mode'
]

if not py3:
    __all__ += ['str', 'bytes']
else:
    __all__ += ['basestring']

