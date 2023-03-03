"""
    0-basic_cache
    BasicCache that inherits from BaseCaching and is a caching system
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    '''
        BasicCache that inherits from BaseCaching
    '''

    def __init__(self) -> None:
        super().__init__()

    def put(self, key, item):
        """ Must assign to the dictionary self.cache_data the item \
            value for the key key
        """
        if key is not None or item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        try:
            return self.cache_data[key]
        except TypeError and KeyError:
            return None
