from contextlib import contextmanager
import sys

from .lazy_proxy_module import LazyProxyModule


class LazyImportHook(object):

    def find_module(self, fullname, path=None):
        return self

    def load_module(self, fullname):
        try:
            return sys.modules[fullname]
        except KeyError:
            mod = LazyProxyModule(fullname)
            sys.modules[fullname] = mod
            return mod


@contextmanager
def lazy_import():
    meta_path = sys.meta_path[:]
    sys.meta_path[:] = [LazyImportHook()]
    try:
        yield
    finally:
        sys.meta_path[:] = meta_path
