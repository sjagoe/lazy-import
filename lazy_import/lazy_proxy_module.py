import importlib
import sys


class LazyImportData(object):
    __slots__ = ('modname', 'module')

    def __init__(self, modname):
        self.modname = modname
        self.module = None

    def real_import(self):
        module = self.module
        if module is None:
            proxy = sys.modules.pop(self.modname)
            try:
                module = importlib.import_module(self.modname)
            finally:
                sys.modules.pop(self.modname, None)
                sys.modules[self.modname] = proxy
            self.module = module
        return module


READABLE_ATTRS = ('__name__', '__path__', '_lazy_import_data')


class LazyProxyModule(object):

    def __init__(self, name):
        object.__setattr__(self, '__name__', name)
        object.__setattr__(self, '__path__', [])
        lazy_import_data = LazyImportData(name)
        object.__setattr__(self, '_lazy_import_data', lazy_import_data)

    def __repr__(self):
        return '<LazyProxyModule name={!r}>'.format(
            self._lazy_import_data.modname)

    def __getattribute__(self, key):
        if key in READABLE_ATTRS:
            return object.__getattribute__(self, key)
        module = self._lazy_import_data.real_import()
        return getattr(module, key)

    def __setattribute__(self, key, value):
        module = self._real_import()
        return setattr(module, key, value)
