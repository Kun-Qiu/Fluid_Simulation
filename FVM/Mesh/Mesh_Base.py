from abc import ABC, abstractmethod

class MeshModel(ABC):
    
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
    def union(self):
        pass

    @abstractmethod
    def intersection(self):
        pass

    @abstractmethod
    def difference(self):
        pass 

    @abstractmethod
    def show(self):
        pass
                