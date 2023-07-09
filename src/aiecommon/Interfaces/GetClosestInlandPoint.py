import geopy
import geopy.distance

class ClosestInlandPoint:
    
    def __init__(self, latitude: float, longitude: float) -> None:
        # Define the distance (in meters) from the original point to the other points
        self.distance_meters = 500
        # Define the sea point as a Shapely Point object
        self.original_point = geopy.Point(latitude, longitude)
        # Calculate distances
        self._calculate_distances()

    def _calculate_distances(self):
        # Define a general distance object, initialized with a distance in km.
        d = geopy.distance.distance(kilometers=self.distance_meters / 1000)
        # Calculate the coordinates of the new points
        self.north_point = d.destination(point=self.original_point, bearing=0)
        self.south_point = d.destination(point=self.original_point, bearing=180)
        self.east_point  = d.destination(point=self.original_point, bearing=90)
        self.west_point  = d.destination(point=self.original_point, bearing=270)
        
    def get_points(self) -> tuple:
        return (
            self.north_point,
            self.south_point,
            self.east_point,
            self.west_point
        )