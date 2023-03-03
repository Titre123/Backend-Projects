#!/usr/bin/env python3
"""Simple pagination sample.
"""
import csv
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int]:
    """Retrieves the index range from a given page and page size.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return tuple([start_index, end_index])


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieves a page of data.
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        range = index_range(page, page_size)
        self.dataset()
        if range[0] > len(self.__dataset):
            return []
        return self.__dataset[range[0]:range[1]]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        '''
            Args:
                - page: int
                - page_size: int
            return
                - List
        '''
        self.dataset()
        total_pages = len(self.__dataset) // page_size
        if (len(self.__dataset) % page_size != 0):
            total_pages += 1
        prev_page = None
        next_page = None
        if page > 1:
            prev_page = page - 1
        if page < total_pages:
            next_page = page + 1
        data = self.get_page(page, page_size)
        return {
            'page_size': page_size,
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
