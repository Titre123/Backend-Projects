#!/usr/bin/python3
"""
    0-basic_cache
    BasicCache that inherits from BaseCaching and is a caching system
"""


BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    '''
        BasicCache that inherits from BaseCaching
    '''

    def __init__(self) -> None:
        self.priority = {}
        super().__init__()

    def put(self, key, item):
        """ Must assign to the dictionary self.cache_data the item \
            value for the key key
        """

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if key not in self.cache_data:
                min = sorted(list(self.priority.values()))[0]
                print(min)
                for k in self.priority.keys():
                    print(k)
                    if self.priority[k] == min:
                        self.cache_data.pop(k)
                        self.priority.__delattr__(k)
                        print('DISCARD: {}'.format(k))
                        break

        if key is not None or item is not None:
            self.cache_data[key] = item
            self.priority[key] = 0
            print(self.priority)

    def get(self, key):
        """ Get an item by key
        """
        self.priority[key] += 1
        try:
            return self.cache_data[key]
        except TypeError and KeyError:
            return None
