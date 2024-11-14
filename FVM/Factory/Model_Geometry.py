import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon
from FVM.Mesh import Mesh_2D


class ModelManager:
    def __init__(self):
        self._shapes = gpd.GeoDataFrame(columns=["Name", "geometry"], crs="EPSG:4326")
        self._size = 0
        self._mesh = Mesh_2D.Mesh2D()

    def __add(self, shape, name=None):
        """
        Add a new polygon / shape to the model manager
        
        :param shape            : Shape
        :param name             : Name of Shape
        :return                 : None
        """
        try:
            new_shape = gpd.GeoDataFrame({"Name": [name], "geometry": [shape]}, crs="EPSG:4326")
            self._shapes = pd.concat([self._shapes, new_shape], ignore_index=True)
            self._size += 1
            return (self._size - 1)
        except:
            raise ValueError("Failed to add the new shape") 


    def __replace(self, shape_idx, shape, name=None):
        """
        Replace a shape in the domain with another shape.
        
        :param shape_idx     :  Index of shape in list
        :param shape         :  The input shape
        :param name          :  Name of polygon
        :return              :  None
        """

        if 0 <= shape_idx < len(self._shapes):
        # Replace the geometry and optionally the type
            self._shapes[shape_idx]["geometry"] = shape
        
            if name is not None:
                self._shapes[shape_idx]["Name"] = name
        else:
            raise IndexError(f"Shape at index {shape_idx} not found.")
        

    def __clear_all(self):
        """
        Clear all shapes in the model manager.
        
        :return     : Previous shapes
        """

        prev_shapes = self._shapes.copy()
        self._shapes = gpd.GeoDataFrame(columns=["Name", "geometry"], crs="EPSG:4326")
        self._size = 0
        return prev_shapes
        

    def delete(self, shape_idx_arr):
        """
        Delete shapes by their unique indices.

        :param shape_idx_arr: Array of indices of shapes to delete.
        :return: List of geometries of the deleted shapes.
        """
        shape_idx_arr = sorted(shape_idx_arr, reverse=True)

        shapes = [self.get_geometry(shape_idx) for shape_idx in shape_idx_arr]
        for shape_idx in shape_idx_arr:
            if 0 <= shape_idx < len(self._shapes):
                self._shapes = self._shapes.drop(index=shape_idx).reset_index(drop=True)
            else:
                raise IndexError(f"Shape at index {shape_idx} not found.")
        
        self._size -= len(shapes)
        return shapes

    
    def replace(self, shape_idx, shape, name=None):
        """
        Replace a shape in the domain with another shape.
        
        :param shape_idx     :  Index of shape in list
        :param shape         :  The input shape
        :param name          :  Name of polygon
        :return              :  None
        """
        self.__replace(shape_idx, shape, name)

    
    def list_all_geometry(self):
        """
        List all the geometry in console
        """

        print(self._shapes)

    
    def get_geometry(self, shape_idx):
        """
        Get the geometry in the model manager at a specified index
        
        :param shape_idx     :  Index of shape in list
        :return              :  geometry of shape at index
        """
        if shape_idx in self._shapes.index:
            return self._shapes.iloc[shape_idx]["geometry"]
        else:
            raise ValueError(f"Shape with index {shape_idx} does not exist.")
        
    
    def getBounds(self):
        """
        Returning the bounds of the geometry
        
        :return     : Bounds of the geometry
        """
        union_idx = self.union_all()
        shape = self._shapes.geometry.iloc[union_idx].bounds
        return self._shapes.geometry.iloc[union_idx].bounds

    
    def showMesh(self):
        """
        Show the mesh using matplotlib
        """
        self._mesh.show()


    def generateMesh(self):
        self._mesh.generate()

    
    def refineMesh(self, iter=1):
        """
        Refine Mesh
        """
        for i in range(iter):
            self._mesh.refine()

    
    def show(self):
        """
        Plot all shapes in the Model Manager.
        
        :return:    None
        """

        if not self._shapes.empty:
            ax = self._shapes.plot(edgecolor="black", alpha=0.5)
            ax.set_aspect('equal')
            plt.show()
        else:
            raise ValueError("There are no shapes to be plotted.")
        

    # ------------------------------------Geometries------------------------------------------ #

    def add_rectangle(self, length: float, height: float, x: float = 0, y: float = 0):
        """   

        :param height           :   Height of square
        :param length           :   Length of rectangle
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   Index of added polygon
        """
        
        half_height: float = height / 2
        half_length: float = length / 2
        rectangle = Polygon([(x - half_length, y - half_height),
                             (x + half_length, y - half_height),
                             (x + half_length, y + half_height),
                             (x - half_length, y + half_height)])
        
        self._mesh.addRectangle([x - half_length, y - half_height, 0], length, height)
        return self.__add(rectangle, f"Rectangle {self._size}")

    
    def add_square(self, side_length: float, x: float = 0, y: float = 0):
        """
        Add a square to the model manager 

        :param side_length      :   Side length of square
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   Index of added polygon
        """

        self._mesh.addRectangle([x - side_length / 2, y - side_length / 2, 0], side_length, side_length)
        return self.add_rectangle(side_length, side_length, x, y)

    
    def add_circle(self, radius: int, x: int = 0, y: int = 0):
        """
        Add a circle to the model manager

        :param radius           :   Radius of cicle
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   Index of added polygon
        """
        
        circle = Point(x, y).buffer(radius)
        self._mesh.addCircle([x, y, 0], radius)
        return self.__add(circle, f"Circle {self._size}")

    
    def add_polygon(self, points):
        """
        Add a polygon defined by a list of (x, y) tuples.
        
        :param points   :   Points that defines the polygon
        :return         :   Index of added polygon
        """
        polygon = Polygon(points)
        self._mesh.addPolygon(points)
        return self.__add(polygon, f"Polygon {self._size}")

    def union(self, idx_1, idx_2):
        """
        Union the first idx shape with the second idx shape
        
        :param idx_1    :   Index of first shape
        :param idx_2    :   Index of second shape
        :return         :   Index of union shape
        """

        try:
            shape_1 = self._shapes.loc[idx_1, "geometry"]
            shape_2 = self._shapes.loc[idx_2, "geometry"]
            union = shape_1.union(shape_2)
            self._mesh.union(idx_1=idx_1, idx_2=idx_2)
            _ = self.delete([idx_1, idx_2])
            return self.__add(union, f"Union {self._size}")
        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")

    
    def union_all(self):
        """
        Union all of the shapes currently stored.
        
        :return     : Index of unioned shape
        """

        union = self._shapes.unary_union
        self.__clear_all()
        return(self.__add(union, name=f"Union {self._size}"))

    
    def intersection(self, idx_1, idx_2):
        """
        Intersection operation between the first idx shape with the second idx shape
        
        :param idx_1    : Index of first shape
        :param idx_2    : Index of second shape
        :return         : Index of intersection shape
        """
        
        try:
            shape_1 = self._shapes.loc[idx_1, "geometry"]
            shape_2 = self._shapes.loc[idx_2, "geometry"]
            intersect = shape_1.intersection(shape_2)
            self._mesh.intersection(idx_1, idx_2)
            _ = self.delete([idx_1, idx_2])
            return(self.__add(intersect, name=f"Difference {self._size}"))
        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")

    
    def intersect_all(self):
        """
        Intersection operation on all of the shapes currently stored.
        
        :return     : Index of intersected shape
        """

        if self._shapes.empty:
            raise ValueError("No shapes available for intersection.")

        intersect = self._shapes.geometry.iloc[0]
        for geom in self._shapes.geometry.iloc[1:]:
            intersect = intersect.intersection(geom)

            if intersect.is_empty:
                break

        self.__clear_all()
        return(self.__add(intersect, name=f"Intersect {self._size}"))

    
    def difference(self, idx_1, idx_2):
        """
        Difference operation between the first idx shape with the second idx shape
       
       :param idx_1     : Index of first shape
       :param idx_2     : Index of second shape
       :return          : Index of the difference shape
       """

        try:
            shape_1 = self._shapes.loc[idx_1, "geometry"]
            shape_2 = self._shapes.loc[idx_2, "geometry"]
            diff = shape_1.difference(shape_2)
            self._mesh.difference(idx_1, idx_2)
            self.delete([idx_1, idx_2])
            return self.__add(diff, name=f"Difference {self._size}")
        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")
