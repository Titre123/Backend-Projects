#!/usr/bin/python3
"""
    0-basic_cache
    BasicCache that inherits from BaseCaching and is a caching system
"""


BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    '''
        BasicCache that inherits from BaseCaching
    '''

    def __init__(self) -> None:
        self.last_key = ''
        super().__init__()

    def put(self, key, item):
        """ Must assign to the dictionary self.cache_data the item \
            value for the key key
        """

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if key not in self.cache_data:
                self.cache_data.pop(self.last_key)
                print('DISCARD: {}'.format(self.last_key))

        if key is not None or item is not None:
            self.last_key = key
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        try:
            return self.cache_data[key]
        except TypeError and KeyError:
            return None
