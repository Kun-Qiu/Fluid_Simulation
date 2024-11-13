from abc import ABC, abstractmethod

class MeshModel(ABC):

    def __init__(self):
        pass
    
    @abstractmethod
    def addPolygon(self, ptsList):
        pass

    @abstractmethod
    def addCircle(self, pt, r):
        pass
    
    @abstractmethod
    def addRectangle(self, pt, l, h):
        pass

    @abstractmethod
    def union(self, idx_arr):
        pass

    @abstractmethod
    def intersection(self, idx_arr):
        pass

    @abstractmethod
    def difference(self, idx_1, idx_2):
        pass 

    @abstractmethod
    def show(self):
        pass
                