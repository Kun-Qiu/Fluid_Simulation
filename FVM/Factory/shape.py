from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, vertices):
        self.CENTROID = None
        self.VERTICES = vertices
        self.CONNECTIVITY = None
        self.VOLUME = None

    @abstractmethod
    def calcCellCentroid(self):
        """Calculate and return the centroid of the shape."""
        pass

    @abstractmethod
    def calcEdges(self):
        """Calculate and return the edges of the shape."""
        pass

    @abstractmethod
    def defConnectivity(self):
        """Define the connectivity of the shape's nodes or edges."""
        pass

    @abstractmethod
    def calcVolume(self):
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def calcPerimeter(self):
        """Calculate the perimeter of the shape."""
        pass
