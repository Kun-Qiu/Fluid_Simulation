import numpy as np


def dcircle(pts, xc, yc, r):
    """
    Distance function for the circle centered at (xc, yc)

    :param pts  :   Points
    :param xc   :   Center X
    :param yc   :   Center Y
    :param r    :   Radius
    :return     :   Distance from Circle
    """
    return np.sqrt((pts[:, 0] - xc) ** 2 + (pts[:, 1] - yc) ** 2) - r


def drectangle(pts, x1, x2, y1, y2):
    """
    Distance function for the rectangle with domain (x1, x2), range (y1, y2)

    :param pts  :   Points
    :param x1   :   X_min
    :param x2   :   X_max
    :param y1   :   Y_min
    :param y2   :   Y_max
    :return     :   Distance function
    """
    return -np.minimum(np.minimum(np.minimum(-y1 + pts[:, 1], y2 - pts[:, 1]), -x1 + pts[:, 0]),
                       x2 - pts[:, 0])


def ddiff(d1, d2):
    """
    Distance function for the difference of two sets

    :param d1   :   Distance function of shape 1
    :param d2   :   Distance function of shape 2
    :return     :   Max of two distance function
    """
    return np.maximum(d1, -d2)


def dintersect(d1, d2):
    """
    Distance function for the intersection of two sets

    :param d1   :   Distance function of shape 1
    :param d2   :   Distance function of shape 2
    :return     :   Max of two distance function
    """
    return np.maximum(d1, d2)


def dunion(d1, d2):
    """
    Distance function for the union of two sets

    :param d1   :   Distance function of shape 1
    :param d2   :   Distance function of shape 2
    :return     :   Minimum of distance function
    """
    return np.minimum(d1, d2)


def huniform(pts, *args):
    """
    Triangle size functions giving near uniform mesh

    :param pts:
    :param args:
    :return:
    """
    return np.ones((pts.shape[0]), 1)

# def dpolygon():
#
#
#
# def boundary
