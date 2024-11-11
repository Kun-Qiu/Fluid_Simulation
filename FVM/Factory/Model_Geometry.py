import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon


class ModelManager:
    def __init__(self):
        # Initialize an empty GeoDataFrame to store shapes with an ID column
        self.shapes = gpd.GeoDataFrame(columns=["id", "type", "geometry"], crs="EPSG:4326")
        self.next_id: int = 0

    def __add(self, shape, shape_type=None):
        """
        Add a new polygon / shape to the model manager
        :param shape            : Shape
        :param shape_type       : Shape Type
        :return                 : None
        """
        new_shape = gpd.GeoDataFrame({"id": [self.next_id], "type": [shape_type], "geometry": [shape]}, crs="EPSG:4326")
        self.shapes = pd.concat([self.shapes, new_shape], ignore_index=True)
        self.next_id += 1

        return self.next_id - 1

    def __replace(self, shape_id, shape, shape_type=None):
        """
        Replace a shape in the domain with another shape
        :param shape_id     :
        :param shape        :
        :param shape_type   :
        :return:
        """
        if shape_id in self.shapes["id"].values:
            self.shapes.loc[self.shapes["id"] == shape_id, ["geometry", "type"]] = [shape, shape_type]
        else:
            raise ValueError(f"Shape with ID {shape_id} not found.")

    def __clear_all(self):
        """
        Clear all shapes in the model manager.
        :return: None
        """
        self.shapes = gpd.GeoDataFrame(columns=["id", "type", "geometry"], crs="EPSG:4326")
        self.next_id = 0

    def delete(self, shape_id):
        """
        Delete a shape by its unique ID
        :param shape_id     : Id of shape
        :return             : Id of deleted shape
        """
        if shape_id in self.shapes["id"].values:
            self.shapes = self.shapes[self.shapes["id"] != shape_id].reset_index(drop=True)
        else:
            raise ValueError(f"Shape with ID {shape_id} not found.")
        return shape_id

    def replace(self, shape_id, shape, shape_type=None):
        self.__replace(shape_id, shape, shape_type)

    # ------------------------------------Geometries------------------------------------------ #
    def list_all_geometry(self):
        print(self.shapes)

    def get_geometry(self, index):
        if index in self.shapes.index:
            return self.shapes.iloc[index]["geometry"]
        else:
            raise ValueError(f"Shape with index {index} does not exist.")

    def add_rectangle(self, length: float, width: float, x: float = 0, y: float = 0):
        """
        :param width            :   Width of square
        :param length           :   Length of rectangle
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   None
        """
        half_width: float = width / 2
        half_length: float = length / 2
        rectangle = Polygon([(x - half_length, y - half_width),
                             (x + half_length, y - half_width),
                             (x + half_length, y + half_width),
                             (x - half_length, y + half_width)])
        return self.__add(rectangle, "Rectangle")

    def add_square(self, side_length: int, x: int = 0, y: int = 0):
        """
        :param side_length      :   Side length of square
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   None
        """
        half_side = side_length / 2
        square = Polygon([(x - half_side, y - half_side),
                          (x + half_side, y - half_side),
                          (x + half_side, y + half_side),
                          (x - half_side, y + half_side)])
        return self.__add(square, "Square")

    def add_circle(self, radius: int, x: int = 0, y: int = 0):
        """
        :param radius           :   Radius of cicle
        :param x                :   X-coordinate of center
        :param y                :   Y-coordinate of center
        :return                 :   None
        """
        circle = Point(x, y).buffer(radius)
        return self.__add(circle, "Circle")

    def add_polygon(self, points):
        """
        Add a polygon defined by a list of (x, y) tuples.
        :param points   :   Points that defines the polygon
        :return         :   None
        """
        polygon = Polygon(points)
        return self.__add(polygon, "Polygon")

    def union(self, idx_1, idx_2):
        """
        Union the first idx shape with the second idx shape
        :param idx_1    :   Index of first shape
        :param idx_2    :   Index of second shape
        :return         :   None
        """

        try:
            shape_1 = self.shapes.loc[idx_1, "geometry"]
            shape_2 = self.shapes.loc[idx_2, "geometry"]
            self.__replace(idx_1, shape_1.union(shape_2), shape_type="Union")
            self.delete(idx_2)

        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")

    def union_all(self):
        """
        Union all of the shapes currently stored.
        :return: None
        """

        union_shape = self.shapes.union_all()
        self.__clear_all()
        self.__add(union_shape, shape_type="Union")

    def intersection(self, idx_1, idx_2):
        """
        Intersection operation between the first idx shape with the second idx shape
        :param idx_1    : Index of first shape
        :param idx_2    : Index of second shape
        :return:
        """

        try:
            shape_1 = self.shapes.loc[idx_1, "geometry"]
            shape_2 = self.shapes.loc[idx_2, "geometry"]
            self.__replace(idx_1, shape_1.intersect(shape_2), shape_type="Intersect")
            self.delete(idx_2)

        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")

    def intersect_all(self):
        """
        Intersection operation on all of the shapes currently stored.
        :return: None
        """

        intersect_shape = self.shapes.intersect_all()
        self.__clear_all()
        self.__add(intersect_shape, shape_type="Intersect")

    def difference(self, idx_1, idx_2):
        """
       Difference operation between the first idx shape with the second idx shape
       :param idx_1     : Index of first shape
       :param idx_2     : Index of second shape
       :return          : None
       """

        try:
            shape_1 = self.shapes.loc[idx_1, "geometry"]
            shape_2 = self.shapes.loc[idx_2, "geometry"]
            self.__replace(idx_1, shape_1.difference(shape_2), "Difference")
            self.delete(idx_2)

        except KeyError:
            print(f"One of the specified indices ({idx_1}, {idx_2}) does not exist.")

    def getBounds(self):
        """
        Returning the bounds of the geometry
        :return: bounds
        """
        union_shape = self.shapes.union_all()
        return union_shape.bounds

    def show(self):
        """
        Plot all shapes in the Model Manager.
        :return:    None
        """
        ax = self.shapes.plot(edgecolor="black", alpha=0.5)
        ax.set_aspect('equal')
        plt.show()
