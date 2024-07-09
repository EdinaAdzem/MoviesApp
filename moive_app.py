from abc import ABC, abstractmethod

class MovieApp (ABC):
    def __init__(self, storage):
        self._storage = storage
        pass
