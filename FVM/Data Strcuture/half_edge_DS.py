class Half_EdgeMesh:
    class Vertex:
        def __init__(self, position, id):
            """
            Vertex element of mesh. Only knows about one of its
            outgoing half-edges.
            :param position     : Spatial position
            :param id           : Unique identification for the vertex
            """
            self.position = position
            self.half_edge = None

        def on_boundary(self):

        def degree(self):

        def normal(self):

        def neighbor_centroid(self):


    class Face:
        """
        Face element of mesh. Only knows one of many half-edges
        circulating around its interior.
        """

        def __init__(self):
            self.half_edge = None
            self.face_normal = None

    class HalfEdge:
        """
        Half edge element of mesh. Knows the twin half-edge, next
        half-edge, vertex, and the face of associated with half-
        edge.
        """

        def __init__(self):
            self.vertex = None
            self.twin = None  # Opposite half-edge (sharing the same edge)
            self.next = None  # Next half-edge around the face
            self.face = None  # Face this half-edge borders
            # self.edge_normal = None
