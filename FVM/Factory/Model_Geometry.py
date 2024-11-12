import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon
import copy


class ModelManager:
    def __init__(self):
        # Initialize an empty GeoDataFrame to store shapes with an ID column
        self.shapes = gpd.GeoDataFrame(columns=["Name", "geometry"], crs="EPSG:4326")
        self.size = 0

    def __add(self, shape, name=None):
        """
        Add a new polygon / shape to the model manager
        
        :param shape            : Shape
        :param name             : Name of Shape
        :return                 : None
        """
        try:
            new_shape = gpd.GeoDataFrame({"Name": [name], "geometry": [shape]}, crs="EPSG:4326")
            self.shapes = pd.concat([self.shapes, new_shape], ignore_index=True)
            self.size += 1
            return (self.size - 1)
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

        if 0 <= shape_idx < len(self.shapes):
        # Replace the geometry and optionally the type
            self.shapes[shape_idx]["geometry"] = shape
        
            if name is not None:
                self.shapes[shape_idx]["Name"] = name
        else:
            raise IndexError(f"Shape at index {shape_idx} not found.")
        

    def __clear_all(self):
        """
        Clear all shapes in the model manager.
        
        :return     : Previous shapes
        """

        prev_shapes = self.shapes.copy()
        self.shapes = gpd.GeoDataFrame(columns=["Name", "geometry"], crs="EPSG:4326")
        self.size = 0
        return prev_shapes
        

    def delete(self, shape_idx_arr):
        """
        Delete a shape by its unique ID
        
        :param shape_idx_arr        : Array of index of shape to delete
        :return                     : geometry of deleted shape
        """
        
        shapes = [self.get_geometry(shape_idx) for shape_idx in shape_idx_arr]
        idx_correction = 0

        for shape_idx in shape_idx_arr:
            shape_idx = shape_idx - idx_correction
            if 0 <= shape_idx < len(self.shapes):
                # Remove the shape and reset indices
                self.shapes = self.shapes.drop(index=shape_idx).reset_index(drop=True)
                self.size -= 1
            else:
                raise IndexError(f"Shape at index {shape_idx} not found.")
            idx_correction += 1

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

        print(self.shapes)

    
    def get_geometry(self, shape_idx):
        """
        Get the geometry in the model manager at a specified index
        
        :param shape_idx     :  Index of shape in list
        :return              :  geometry of shape at index
        """
        if shape_idx in self.shapes.index:
            return self.shapes.iloc[shape_idx]["geometry"]
        else:
            raise ValueError(f"Shape with index {shape_idx} does not exist.")
        
    
    def getBounds(self):
        """
        Returning the bounds of the geometry
        
        :return     : Bounds of the geometry
        """
        union_idx = self.union_all()
        shape = self.shapes.geometry.iloc[union_idx].bounds
        return self.shapes.geometry.iloc[union_idx].bounds

    
    def show(self):
        """
        Plot all shapes in the Model Manager.
        
        :return:    None
        """
        ax = self.shapes.plot(edgecolor="black", alpha=0.5)
        ax.set_aspect('equal')
        plt.show()

    # ------------------------------------Geometries------------------------------------------ #

    def add_rectangle(self, length: float, width: float, x: float = 0, y: float = 0):
        """   

        :param width            :   Width of square
        :param length           :   Length of rectangle
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   Index of added polygon
        """
        
        half_width: float = width / 2
        half_length: float = length / 2
        rectangle = Polygon([(x - half_length, y - half_width),
                             (x + half_length, y - half_width),
                             (x + half_length, y + half_width),
                             (x - half_length, y + half_width)])
        return self.__add(rectangle, f"Rectangle {self.size}")

    
    def add_square(self, side_length: int, x: int = 0, y: int = 0):
        """
        Add a square to the model manager 

        :param side_length      :   Side length of square
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   Index of added polygon
        """

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
        return self.__add(circle, f"Circle {self.size}")

    
    def add_polygon(self, points):
        """
        Add a polygon defined by a list of (x, y) tuples.
        
        :param points   :   Points that defines the polygon
        :return         :   Index of added polygon
        """
        polygon = Polygon(points)
        return self.__add(polygon, f"Polygon {self.size}")

    def union(self, idx_1, idx_2):
        """
        Union the first idx shape with the second idx shape
        
        :param idx_1    :   Index of first shape
        :param idx_2    :   Index of second shape
        :return         :   Index of union shape
        """

        try:
            shape_1 = self.shapes.loc[idx_1, "geometry"]
            shape_2 = self.shapes.loc[idx_2, "geometry"]
            union = shape_1.union(shape_2)
            _ = self.delete([idx_1, idx_2])
            return self.__add(union, f"Union {self.size}")
        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")

    
    def union_all(self):
        """
        Union all of the shapes currently stored.
        
        :return     : Index of unioned shape
        """

        union = self.shapes.unary_union
        self.__clear_all()
        return(self.__add(union, name=f"Union {self.size}"))

    
    def intersection(self, idx_1, idx_2):
        """
        Intersection operation between the first idx shape with the second idx shape
        
        :param idx_1    : Index of first shape
        :param idx_2    : Index of second shape
        :return         : Index of intersection shape
        """
        
        try:
            shape_1 = self.shapes.loc[idx_1, "geometry"]
            shape_2 = self.shapes.loc[idx_2, "geometry"]
            intersect = shape_1.intersect(shape_2)
            _ = self.delete([idx_1, idx_2])
            return(self.__add(intersect, name=f"Difference {self.size}"))
        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")

    
    def intersect_all(self):
        """
        Intersection operation on all of the shapes currently stored.
        
        :return     : Index of intersected shape
        """

        if self.shapes.empty:
            raise ValueError("No shapes available for intersection.")

        intersect = self.shapes.geometry.iloc[0]
        for geom in self.shapes.geometry.iloc[1:]:
            intersect = intersect.intersection(geom)

            if intersect.is_empty:
                break

        self.__clear_all()
        return(self.__add(intersect, name=f"Intersect {self.size}"))

    
    def difference(self, idx_1, idx_2):
        """
        Difference operation between the first idx shape with the second idx shape
       
       :param idx_1     : Index of first shape
       :param idx_2     : Index of second shape
       :return          : Index of the difference shape
       """

        try:
            shape_1 = self.shapes.loc[idx_1, "geometry"]
            shape_2 = self.shapes.loc[idx_2, "geometry"]
            diff = shape_1.difference(shape_2)
            self.delete([idx_1, idx_2])
            return self.__add(diff, name=f"Difference {self.size}")
        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")
