from __future__ import absolute_import

import threading
from .driver_cache import load_drivers


class WriterDriverCache(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls('datacube.plugins.io.write')
        return cls.__singleton_instance

    def __init__(self, group):
        self._drivers = load_drivers(group)

        for driver in list(self._drivers.values()):
            if hasattr(driver, 'aliases'):
                for alias in driver.aliases:
                    self._drivers[alias] = driver

    def __call__(self, name):
        """
        :returns: None if driver with a given name is not found

        :param str name: Driver name
        :param str fmt: Dataset format
        :return: Returns WriterDriver
        """
        return self._drivers.get(name, None)

    def drivers(self):
        """ Returns list of driver names
        """
        return list(self._drivers.keys())


def writer_cache():
    """ Singleton for WriterDriverCache
    """
    return WriterDriverCache.instance()


def writer_drivers():
    """ Returns list driver names
    """
    return writer_cache().drivers()


def storage_writer_by_name(name):
    """ Lookup writer driver by name

    :returns: Initialised writer driver instance
    :returns: None if driver with this name doesn't exist
    """
    return writer_cache()(name)
